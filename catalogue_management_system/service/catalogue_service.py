from util.db_get_connection import get_connection
from dto.catalogue_dto import Catalogue
from exceptions.exceptions import CatalogueNotFoundException, DuplicateCatalogueException

class CatalogueService:
    def create_catalogue(self, catalogue: Catalogue):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Catalogue WHERE catalogue_id = %s", (catalogue.catalogue_id,))
            if cursor.fetchone():
                raise DuplicateCatalogueException("Catalogue already exists.")
            cursor.execute("""
                INSERT INTO Catalogue (catalogue_id, catalogue_name, catalogue_description, start_date, end_date, is_active)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (catalogue.catalogue_id, catalogue.name, catalogue.description,
                  catalogue.start_date, catalogue.end_date, catalogue.is_active))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def get_catalogue_by_id(self, catalogue_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT catalogue_id, catalogue_name, catalogue_description, start_date, end_date, is_active
                FROM Catalogue WHERE catalogue_id = %s
            """, (catalogue_id,))
            row = cursor.fetchone()
            if not row:
                raise CatalogueNotFoundException("Catalogue not found.")
            return Catalogue(*row)
        finally:
            cursor.close()
            conn.close()

    def update_catalogue_by_id(self, catalogue_id, updated_catalogue: Catalogue):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE Catalogue 
                SET catalogue_name = %s, catalogue_description = %s, start_date = %s, end_date = %s, is_active = %s
                WHERE catalogue_id = %s
            """, (
                updated_catalogue.name,
                updated_catalogue.description,
                updated_catalogue.start_date,
                updated_catalogue.end_date,
                updated_catalogue.is_active,
                catalogue_id
            ))
            if cursor.rowcount == 0:
                raise CatalogueNotFoundException("Catalogue not found for update.")
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def delete_catalogue_by_id(self, catalogue_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Catalogue WHERE catalogue_id = %s", (catalogue_id,))
            if cursor.rowcount == 0:
                raise CatalogueNotFoundException("Catalogue not found to delete.")
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def get_all_catalogues(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT catalogue_id, catalogue_name, catalogue_description, start_date, end_date, is_active
                FROM Catalogue
            """)
            rows = cursor.fetchall()
            return [Catalogue(*row) for row in rows]
        finally:
            cursor.close()
            conn.close()
            conn.close()
