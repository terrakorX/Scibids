import sqlite3
from typing import Optional
from loguru import logger


class DatabaseError(Exception):
    pass



def add_headers_sqlite(d, cursor) -> dict:
    headers = [description[0] for description in cursor.description]
    _data = {headers[index]: value for index, value in enumerate(d)}
    return _data


def get_documents(document_id: Optional[int] = None) -> list[dict]:
    """
    Récupère les documents de la base de données SQLite.
    Si un ID de document est fourni, récupère uniquement ce document."""

    documents = []
    logger.debug(f"connection au sqlite pour récupérer le document >{document_id}")
    with sqlite3.connect("document.db") as conn:
        try:
            if document_id:
                cursor = conn.execute('SELECT * FROM document WHERE id = ?', (document_id,))
                data = cursor.fetchall()
            else:
                print(document_id)
                cursor = conn.execute('SELECT * FROM document')
                data = cursor.fetchall()
        except sqlite3.Error as err:
            logger.error(f"Erreur de  connection au sqlite {err.args[0]}")
            raise DatabaseError(err.args[0])
        for d in data:
            documents.append(add_headers_sqlite(d, cursor))

    return documents


def get_tag_by_document_id(tag_id) -> list[dict]:
    """
    Récupère les documents associés à un tag via son ID.
    """
    documents = []
    logger.debug(f"connection au sqlite pour récupérer le document  avec le tag ID >{tag_id}")
    with sqlite3.connect("document.db") as conn:
        try:
            cursor = conn.cursor()
            query = """  
            SELECT 
            GROUP_CONCAT(t.name) AS tags
            FROM document d
            LEFT JOIN document_tag dt ON d.id = dt.document_id
            LEFT JOIN tag t ON t.id = dt.tag_id
            GROUP BY d.id;
            WHERE dt.tag_id = ?
            """
            cursor.execute(query, (tag_id,))
            rows = cursor.fetchall()
            # eliminer les document qui n'ont pas deux versions
            for row in rows:
                for i in rows:
                    if row[1] == i[1] and row[4] == i[4] + 1:
                        documents.append(({
                                  'id': row[0],
                                    'name': row[1],
                                    'number_of_employees': row[2],
                                    'is_serious': bool(row[3]),
                                    'version': row[4]
                            }, {
                                'id': i[0],
                                    'name': i[1],
                                    'number_of_employees': i[2],
                                    'is_serious': bool(i[3]),
                                    'version': i[4]
                            }))
                        rows.remove(i)
            return documents
        except sqlite3.Error as err:
            logger.error(f"Erreur de  connection au sqlite {err.args[0]}")
            raise DatabaseError(f"Database error: {err}")
        
def get_all_documents(document_id: Optional[int] = None) -> list[dict]:
    """
    Récupère tous les documents avec des informations supplémentaires de la base de données SQLite.
    """
    documents = []
    logger.debug(f"connection au sqlite pour récupérer les documents et leurs informations {document_id}")
    with sqlite3.connect("document.db") as conn:
        try:
            if document_id:
                cursor = conn.execute("""SELECT d.id,
                d.name, 
                d.number_of_employees,
                d.is_serious,
                d.version, 
                GROUP_CONCAT(t.name) AS tags 
                FROM document d 
                LEFT JOIN document_tag dt ON d.id = dt.document_id
                LEFT JOIN tag t ON t.id = dt.tag_id
                WHERE d.id = ?
                GROUP BY d.id;""", (document_id,))
                data = cursor.fetchall()
            else:
                cursor = conn.execute("""SELECT d.id,
                d.name, 
                d.number_of_employees,
                d.is_serious,
                d.version, 
                GROUP_CONCAT(t.name) AS tags 
                FROM document d
                LEFT JOIN document_tag dt ON d.id = dt.document_id
                LEFT JOIN tag t ON t.id = dt.tag_id
                GROUP BY d.id;""")
                data = cursor.fetchall()
            for row in data:
                for i in data:
                    if row[1] == i[1] and row[4] == i[4] + 1:
                        documents.append({ 'old' if row[4] ==1 else 'new' : {
                                  'id': row[0],
                                    'name': row[1],
                                    'number_of_employees': row[2],
                                    'is_serious': bool(row[3]),
                                    'version': row[4],
                                    'tags': row[5].split(',')
                            },  'new' if i[4] == 2 else 'old' :{
                                'id': i[0],
                                    'name': i[1],
                                    'number_of_employees': i[2],
                                    'is_serious': bool(i[3]),
                                    'version': i[4],
                                    'tags': i[5].split(',')
                            }})
                        data.remove(i)
            return documents
        except sqlite3.Error as err:
            logger.error(f"Erreur de  connection au sqlite {err.args[0]}")
            raise DatabaseError(err.args[0])
