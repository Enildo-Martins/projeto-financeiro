from .base_repository import BaseRepository


class PessoaRepository(BaseRepository):

    def find_by_documento(self, documento):
        query = """SELECT id FROM "Pessoas" WHERE documento = %s"""
        result = self._execute_query(query, [documento], fetch="one")
        return result[0] if result else None

    def create(self, tipo, detail):
        query = """
            INSERT INTO "Pessoas" (tipo, razaosocial, fantasia, documento, status)
            VALUES (%s, %s, %s, %s, 'ATIVO') RETURNING id
        """
        params = [
            tipo,
            detail.get('razaosocial') or detail.get('razao_social') or detail.get('nome_completo') or detail.get('pessoa_fisica'),
            detail.get('fantasia'),
            detail.get('documento') or detail.get('cnpj') or detail.get('cpf/cnpj')
        ]
        return self._execute_query(query, params)

    def list_all(self):
        query = """
            SELECT id, razaosocial, documento, tipo, status 
            FROM "Pessoas" ORDER BY razaosocial
        """
        return self._execute_query(query, fetch="all")

    def find_by_id(self, pk):
        query = """
            SELECT id, tipo, razaosocial, fantasia, documento 
            FROM "Pessoas" WHERE id = %s
        """
        return self._execute_query(query, [pk], fetch="one")

    def update(self, pk, tipo, razaosocial, fantasia, documento):
        query = """
            UPDATE "Pessoas" SET tipo=%s, razaosocial=%s, fantasia=%s, documento=%s
            WHERE id=%s
        """
        params = [tipo, razaosocial, fantasia, documento, pk]
        self._execute_query(query, params)

    def toggle_status(self, pk):
        query = """
            UPDATE "Pessoas" 
            SET status = CASE WHEN status = 'ATIVO' THEN 'INATIVO' ELSE 'ATIVO' END
            WHERE id = %s
        """
        self._execute_query(query, [pk])

    def list_active_clients(self):
        query = """
            SELECT id, razaosocial FROM "Pessoas" 
            WHERE tipo IN ('CLIENTE', 'FATURADO') AND status = 'ATIVO' ORDER BY razaosocial
        """
        return self._execute_query(query, fetch="all")
    
    def list_all_active(self, order_by='razaosocial'):
        order_sql = self._get_order_clause(order_by)
        query = f"""
            SELECT id, razaosocial, documento, tipo, status 
            FROM "Pessoas" 
            WHERE status = 'ATIVO' 
            ORDER BY {order_sql}
        """
        return self._execute_query(query, fetch="all")

    def search_active(self, termo, order_by='razaosocial'):
        order_sql = self._get_order_clause(order_by)
        query = f"""
            SELECT id, razaosocial, documento, tipo, status 
            FROM "Pessoas" 
            WHERE (razaosocial ILIKE %s OR documento ILIKE %s)
            AND status = 'ATIVO'
            ORDER BY {order_sql}
        """
        param = f"%{termo}%"
        return self._execute_query(query, [param, param], fetch="all")
    
    def _get_order_clause(self, order_param):
        """
        Traduz o parâmetro de ordenação da URL para SQL seguro.
        Evita SQL Injection validando contra uma lista permitida.
        """
        mapeamento = {
            'razaosocial': 'razaosocial ASC',
            '-razaosocial': 'razaosocial DESC',
            'documento': 'documento ASC',
            '-documento': 'documento DESC',
            'tipo': 'tipo ASC',
            '-tipo': 'tipo DESC',
            'status': 'status ASC',
            '-status': 'status DESC'
        }
        return mapeamento.get(order_param, 'razaosocial ASC')