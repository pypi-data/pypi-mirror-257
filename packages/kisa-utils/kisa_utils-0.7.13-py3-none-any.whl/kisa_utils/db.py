import os, sys
import sqlite3
from types import SimpleNamespace

from . import storage

if sqlite3.sqlite_version_info[1]<38:
    sys.exit(f'we need sqlite3 v3.38.0+ to run this program. current version::{sqlite3.sqlite_version}')

MAX_FETCH_ITEMS = 8*1024

__EXT__ = 'sqlite3'

# you want this to throw erros in user-defined functions
sqlite3.enable_callback_tracebacks(True)

TRIGGERS:dict = {
    # eg
    # 'userActiveStateChange':{
    #     'table': 'users',
    #     'when': 'after', # before | after | instead of
    #     'action': 'update', # insert | update | delete
    #     'condition':'''
    #         old.active != new.active
    #     ''',
    #     'code':'''
    #         insert into logs values(
    #             datetime('now', '+03:00'), 
    #             new.addedBy, 
    #             "users.active: change "||old.active||"->"||new.active,
    #             "{}"
    #         )
    #     '''
    # },

}

# *********************************************************************
def _checkContext(method):
    '''
    this decorator will be used to enforce the calling of Api class instances
    from `with` contexts. this will ensure resources are always released as they
    should
    '''
    def _(self, *args, **kwargs):
        if not self._in_with_statement:
            raise Exception(f'method `db.Api.{method.__name__}` called from outside `with` statement/context')
        if method.__name__ in ['insert','update','delete'] and self._readonly:
            return {
                'status':False,
                'log': f'calling a write method (`db.Api.{method.__name__}`) on a read-only database'
            }
            # raise Exception(f'calling a write method (`db.Api.{method.__name__}`) on a read-only database')
        return method(self,*args, **kwargs)
    return _

class Api:
    def __init__(
        self, 
        path:str=':memory:', 
        tables:dict = {}, 
        readonly:bool=True, 
        bindingFunctions:list=[],
        transactionMode:bool = False
    ):
        '''
        attempt to open an sqlite3 database connection

        @param `path`: path to the database file. if;
            + `path` does not exist and it does not end with the `.sqlite3` extension, it will be added`
            
            + `path` is set to `':memory:'`, an in-memory db will be opened and `readonly` will automatically be set to False
        
        @param `tables`: dict[str,str]
                eg
                {
                    'credentials':"""
                        key             varchar(256) not null,
                        value           varchar(256) not null
                    """,
                    'users':"""
                        firstName       varchar(256) not null,
                        lastName        varchar(256) not null,
                        username        varchar(256) not null
                    """,
                }

        @param `readonly`: flag indicating if the database should be opened in read-only mode.
            + if `path` is set to `':memory:'`, `readonly` will automatically be reset to False

        @param `bindingFunctions`:  Custom functions defined in python to be used by sqlite3. 
            + Each entry is in form (name:str, nargs:int, func:py-function)

        '''

        self._in_with_statement = False
        self.isOpen = False
        self.functions:dict = {}
        
        self.transactionMode = True if transactionMode else False

        if ':memory:' != path:
            while path.endswith('/'): path = path[:-1]
            if not path.endswith(f'.{__EXT__}') and not os.path.isfile(path):
                path += f'.{__EXT__}'

            path_root = os.path.split(path)[0]
            
            if (not os.path.isdir(path_root)) and os.system(f'mkdir -p "{path_root}"'):
                return

            if not os.path.isfile(path):
                initTables = True
        
        readonly = False if (':memory:' == path or self.transactionMode) else readonly

        self._readonly = True if readonly else False 

        self.db:sqlite3.Connection = sqlite3.connect(path)
        if self.transactionMode:
            self.db.isolation_level = None
        self.cursor:sqlite3.Cursor = self.db.cursor();

        initTables = True if tables else False
        if initTables:
            self.__startTransaction()
            for table in tables:
                self.cursor.execute(f'create table if not exists {table} ({tables[table]})')
            if self.transactionMode:
                self.db.commit()
            else:
                self.__commit()
        
        self._bind_functions(bindingFunctions)
        
        self.isOpen = True

        self.__startTransaction()

        if readonly:
            self.cursor.execute(f'''
            pragma query_only = ON;   -- disable changes
            ''')

    def _bind_functions(self, functions):
        for entry in functions:
            if entry[0] in self.functions: continue
            self.db.create_function(*entry)
            self.functions[entry[0]] = entry[-1]

    def __startTransaction(self):
        if self.transactionMode:
            self.cursor.execute('begin')
            self._transactionData = {
                op:{'passed':0, 'failed':0}
                for op in ['insert','delete','update']
            }

    def __commit(self):
        '''
        attempt to commit to the database IF its not open in `transactionMode=True`
        '''
        if not self.transactionMode:
            self.db.commit()

    @_checkContext
    def execute(self, cmd:str, cmdData:list=[], commit:bool=False) -> dict[str,bool|str]:
        reply = {'status':False, 'log':''}

        try:
            self.cursor.execute(cmd,cmdData)
            if commit: self.__commit() # ?
        except Exception as e:
            reply['log'] = str(e)
            return reply

        reply['status'] = True
        return reply

    @_checkContext
    def fetch(self, table:str, columns:list, condition:str, conditionData:list, limit:int=MAX_FETCH_ITEMS, returnDicts:bool=False, returnNamespaces:bool=False) -> list:
        '''
        fetch databse data given condition and conditionValues eg
        
        apiObj.fetch(
            'users',
            ['username','clearance'],
            'active=? and username=? and password=?',
            [1,'test','123']
        )
        '''
        assert (limit>0 and limit<=MAX_FETCH_ITEMS), f'please set a limit on the returned rows. maximum should be {MAX_FETCH_ITEMS}'

        condition = condition.strip() or '1'
        assert(len(condition.strip()))
        
        if columns in [['*']]:
            self.cursor.execute(f'select * from {table} where {condition} limit {limit}',conditionData)
            columns = [description[0] for description in self.cursor.description]

        self.cursor.execute(f"select {','.join(columns)} from {table} where {condition} limit {limit}",conditionData)
        
        if not (returnDicts or returnNamespaces):
            return self.cursor.fetchall()

        cols = [_[0] for _ in self.cursor.description]

        if returnDicts:
            return [dict(zip(cols,_)) for _ in self.cursor.fetchall()]

        # namepsaces...
        if [_ for _ in cols if (
            (' ' in _) or not (
                'a'<=_[0]<='z' or \
                'A'<=_[0]<='Z' or \
                '_'==_[0]
            )
        )]:
            raise TypeError('one or more column names is invalid as a key for namespaces')

        return [SimpleNamespace(**dict(zip(cols,_))) for _ in self.cursor.fetchall()]

    @_checkContext
    def insert(self, table:str, data:list) -> dict[str,bool|str]:
        self.cursor.execute(f'select * from {table}')
        column_value_placeholders = ['?' for description in self.cursor.description]
        
        reply = {'status':False, 'log':''}
        try:
            if isinstance(data[0],list) or isinstance(data[0],tuple):
                self.cursor.executemany(f'insert into {table} values ({",".join(column_value_placeholders)})',data)
            else:
                self.cursor.execute(f'insert into {table} values ({",".join(column_value_placeholders)})',data)
            self.__commit()
            if self.transactionMode: self._transactionData['insert']['passed'] += 1
        except Exception as e:
            if self.transactionMode: self._transactionData['insert']['failed'] += 1
            reply['log'] = str(e)
            return reply

        reply['status'] = True
        return reply

    @_checkContext
    def update(self, table:str, columns:list, columnData:list, condition:str, conditionData:list) -> dict[str,bool|str]:
        reply = {'status':False, 'log':''}

        if columns in [['*']]:
            self.cursor.execute(f'select * from {table}')
            columns = [description[0] for description in self.cursor.description]

        condition = condition.strip() or '1'
        assert(len(condition.strip()))

        try:
            self.cursor.execute(f'update {table} set {"=?,".join(columns)}=? where {condition}',columnData+conditionData)
            self.__commit()
            if self.transactionMode: self._transactionData['update']['passed'] += 1
        except Exception as e:
            if self.transactionMode: self._transactionData['update']['failed'] += 1
            reply['log'] = str(e)
            return reply

        reply['status'] = True
        return reply

    @_checkContext
    def delete(self, table:str, condition:str, conditionData:list) -> dict[str,bool|str]:
        reply = {'status':False, 'log':''}

        if not condition.strip():
            if self.transactionMode: self._transactionData['delete']['failed'] += 1
            reply['log'] = 'please provide a delete condition. use `1` if tyou want all data gone'
            return reply

        try:
            self.cursor.execute(f'delete from {table} where {condition}',conditionData)
            self.__commit()
            if self.transactionMode: self._transactionData['delete']['passed'] += 1
        except Exception as e:
            if self.transactionMode: self._transactionData['delete']['failed'] += 1
            reply['log'] = str(e)
            return reply

        reply['status'] = True
        return reply

    @_checkContext
    def close(self):
        if self.isOpen:
            self.db.execute('pragma optimize;')
            if self.transactionMode:
                commit = True
                for op in self._transactionData:
                    if self._transactionData[op]['failed']:
                        commit = False
                        break
                if commit: self.cursor.execute('commit')
            else:
                self.db.commit()

            self.db.close()
            # self.db, self.cursor = None,None
            self.isOpen = False

    @_checkContext
    def release(self):
        return self.close()

    # methods to add context to the handle
    def __enter__(self) -> 'Api':
        self._in_with_statement = True
        return self

    def __exit__(self, *args) -> bool:
        # args = [exc_type, exc_value, traceback]
        self.release()
        self._in_with_statement = False

        # False=propagate exceptions, True=supress them
        # you want to propagate exceptions so that the calling code can know what went wrong
        if args[0] is None:
            return True
        else:
            return False

if __name__=='__main__':
    with Api('/tmp/bukman/database.db2') as handle:
        print(handle.fetch('keys',['*'],'',[]))