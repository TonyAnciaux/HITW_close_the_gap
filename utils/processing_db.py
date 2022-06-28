import os
import logging

import pandas as pd
import mysql.connector
import sshtunnel
from sshtunnel import SSHTunnelForwarder




class DbProcess():
    """
    A Class that handles the processing of the database.
    """

    def __init__(self, host:str) -> None:
        """
        A constructor for the DbProcess class.
        """
        self.is_connected: bool = False
        self.__db_name: str = "HITW_CTG"
        self.__host: str = host
        self.__user: str = "db_write"
        self.__password: str = "Write!Woods!2022@"
        self.__cnx: mysql.connector.connect = None

        self.__ssh_host: str = ""
        self.__ssh_username: str = ""
        self.__ssh_password: str = ""
        self.tunnel: SSHTunnelForwarder = None
    

    def connect(self) -> None:
        """
        A Function that connects to the database.
        """
        try:
            self.__cnx = mysql.connector.connect(
                host=self.__host,
                user=self.__user,
                password=self.__password,
                database=self.__db_name,
                port=self.tunnel.local_bind_port
            )
            self.is_connected = True
        except mysql.connector.Error as err:
            print(err)
            self.is_connected = False
        
    def insert_from_df(self, df: pd.DataFrame) -> int:
        """
        A Function that inserts the data from a dataframe's all lines into the database.
        param: df: A dataframe that contains the data to be inserted.
        return: The number of rows inserted.
        """
        try:
            if not self.is_connected:
                self.connect()
            cursor = self.__cnx.cursor()
            for i in range(len(df)):
                cursor.execute(
                    ""
                )
            self.__cnx.commit()
            cursor.close()
            self.__cnx.close()
            self.is_connected = False
            return self.__cnx.rowcount
        except mysql.connector.Error as err:
            print(err)
            self.is_connected = False
            return 0

    def open_ssh_tunnel(self, verbose=False) -> None:
        """
        A Function that opens a ssh tunnel to the database.
        :param verbose: Set to True to show logging.
        """
        try:
            self.tunnel = SSHTunnelForwarder(
                (self.__ssh_host, 22),
                ssh_username=self.__ssh_username,
                ssh_password=self.__ssh_password,
                remote_bind_address=('', 3306)
            )
            self.tunnel.start()
        except Exception as err:
            print(err)
            self.tunnel = None
""" @Connection Testing
dbProcess = DbProcess("161.35.149.68")
dbProcess.connect()
print(dbProcess.is_connected)
"""
