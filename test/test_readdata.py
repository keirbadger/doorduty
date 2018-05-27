from doorduty.readdata import ReadData
from mock import patch, MagicMock, call
import unittest
from doorduty import config
import datetime


class TestData(unittest.TestCase):
    @patch('pymysql.connect')
    def test_data_init(self, connect_mock):

        ReadData()

        self.assertEqual(1, connect_mock.call_count)

        self.assertEqual(connect_mock.call_args_list[0], call(
            host="localhost",
            user=config.AS_DB_USER,
            passwd=config.AS_DB_PASS,
            database=config.AS_DB_NAME,
            port=config.AS_DB_PORT))

    @patch('doorduty.readdata.pymysql')
    def test_read_duties(self, mock_pymysql):
        mock_cursor = MagicMock()
        test_data = [{12420, 194, 1, datetime.date(2018, 5, 29)}]
        mock_cursor.fetchall.return_value = test_data
        mock_pymysql.connect.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        data = ReadData()
        rtn = data.read_duties()
        print (len(rtn))
        self.assertEquals(self, isinstance(rtn, list))
