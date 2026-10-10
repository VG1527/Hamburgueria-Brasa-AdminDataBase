# =====================================================================
#  SUAS RESPOSTAS
# =====================================================================
#  Escreva cada consulta SQL entre as aspas triplas, assim:
#
#      Q1 = """
#      SELECT ...
#      FROM ...
#      """
#
#  Depois salve o arquivo (Ctrl+S) e veja o resultado no painel.
#  Mexa só no que está ENTRE as aspas triplas.
# =====================================================================

# ---------------------------------------------------------------------
#  NÍVEL 1 - AQUECIMENTO
# ---------------------------------------------------------------------

# Q1. Clientes no Centro
# Colunas do resultado: ClientesNoCentro
Q1 = """
SELECT COUNT(*) AS ClientesNoCentro
FROM Clientes
WHERE Bairro = 'Centro';
"""

# Q2. Hambúrgueres acima de R$ 30
# Colunas do resultado: NomeProduto, Preco
Q2 = """
SELECT NomeProduto, Preco
FROM Produtos
WHERE Categoria = 'Hambúrguer'
AND Preco > 30
ORDER BY Preco DESC;
"""

# Q3. Pedidos por status
# Colunas do resultado: Status, QuantidadePedidos
Q3 = """
SELECT
    Status,
    COUNT(*) AS TotalPedidos
FROM Pedidos
GROUP BY Status;
"""

# Q4. Nota média e pedidos sem avaliação
# Colunas do resultado: PedidosEntregues, PedidosAvaliados, PedidosSemAvaliacao, NotaMedia
Q4 = """
SELECT
COUNT(*)                                   AS PedidosEntregues,
COUNT(Avaliacao)                           AS PedidosAvaliados,
COUNT(*) - COUNT(Avaliacao)                AS PedidosSemAvaliacao,
AVG(Avaliacao)       AS NotaMedia
FROM Pedidos
WHERE Status = 'Entregue';
"""

# Q5. Delivery x Retirada por mês
# Colunas do resultado: Mes, TipoEntrega, QuantidadePedidos
Q5 = """
SELECT
    MONTH(DataPedido) AS Mes,
    TipoEntrega,
    COUNT(*) AS TotalPedidos
FROM Pedidos
WHERE Status = 'Entregue'
GROUP BY MONTH(DataPedido), TipoEntrega
ORDER BY Mes, TipoEntrega;

"""

# ---------------------------------------------------------------------
#  NÍVEL 2 - CRUZANDO TABELAS
# ---------------------------------------------------------------------

# Q6. Pedidos de janeiro com cliente
# Colunas do resultado: IdPedido, DataPedido, Nome, Bairro, Status
Q6 = """
SELECT
    P.IdPedido,
    P.DataPedido,
    C.Nome AS NomeCliente,
    C.Bairro,
    P.Status
FROM Pedidos P
INNER JOIN Clientes C
    ON P.IdCliente = C.IdCliente
WHERE P.DataPedido BETWEEN '2026-01-01' AND '2026-01-31'
ORDER BY P.DataPedido;
"""

# Q7. Entregas por entregador
# Colunas do resultado: Nome, Entregas
Q7 = """
SELECT
    E.Nome AS Entregador,
    COUNT(P.IdPedido) AS TotalEntregas
FROM Pedidos P
INNER JOIN Entregadores E
    ON P.IdEntregador = E.IdEntregador
WHERE P.Status = 'Entregue'
GROUP BY E.Nome
ORDER BY TotalEntregas DESC;
"""

# Q8. Unidades e faturamento por produto
# Colunas do resultado: NomeProduto, UnidadesVendidas, Faturamento
Q8 = """
SELECT
    PR.NomeProduto,
    SUM(IP.Quantidade) AS UnidadesVendidas,
    SUM(IP.Quantidade * IP.PrecoUnitario) AS Faturamento
FROM ItensPedido IP
INNER JOIN Produtos PR
    ON IP.IdProduto = PR.IdProduto
INNER JOIN Pedidos P
    ON IP.IdPedido = P.IdPedido
WHERE P.Status = 'Entregue'
GROUP BY PR.NomeProduto
ORDER BY UnidadesVendidas DESC;
"""

# Q9. Faturamento por categoria
# Colunas do resultado: Categoria, Faturamento
Q9 = """
SELECT
    PR.Categoria,
    SUM(IP.Quantidade * IP.PrecoUnitario) AS Faturamento
FROM ItensPedido IP
INNER JOIN Produtos PR
    ON IP.IdProduto = PR.IdProduto
INNER JOIN Pedidos P
    ON IP.IdPedido = P.IdPedido
WHERE P.Status = 'Entregue'
GROUP BY PR.Categoria
ORDER BY Faturamento DESC;
"""

# Q10. Bairros com 7+ pedidos entregues
# Colunas do resultado: Bairro, PedidosEntregues
Q10 = """
SELECT
    C.Bairro,
    COUNT(P.IdPedido) AS TotalPedidos
FROM Pedidos P
INNER JOIN Clientes C
    ON P.IdCliente = C.IdCliente
WHERE P.Status = 'Entregue'
GROUP BY C.Bairro
HAVING COUNT(P.IdPedido) >= 7
ORDER BY TotalPedidos DESC;

"""

# Q11. Preços praticados do X-Bacon
# Colunas do resultado: PrecoUnitario, Unidades, Faturamento
Q11 = """
SELECT
    IP.PrecoUnitario,
    SUM(IP.Quantidade) AS UnidadesVendidas,
    SUM(IP.Quantidade * IP.PrecoUnitario) AS Faturamento
FROM ItensPedido IP
INNER JOIN Produtos PR
    ON IP.IdProduto = PR.IdProduto
INNER JOIN Pedidos P
    ON IP.IdPedido = P.IdPedido
WHERE PR.NomeProduto = 'X-Bacon'
    AND P.Status = 'Entregue'
GROUP BY IP.PrecoUnitario
ORDER BY IP.PrecoUnitario;
"""

# ---------------------------------------------------------------------
#  NÍVEL 3 - DESAFIO
# ---------------------------------------------------------------------

# Q12. Top 3 clientes (fidelidade)
# Colunas do resultado: Nome, Pedidos, TotalGasto
Q12 = """
SELECT TOP 3
    C.Nome AS Cliente,
    COUNT(DISTINCT P.IdPedido) AS TotalPedidos,
    SUM(IP.Quantidade * IP.PrecoUnitario) AS TotalGasto
FROM Clientes C
INNER JOIN Pedidos P
    ON C.IdCliente = P.IdCliente
INNER JOIN ItensPedido IP
    ON P.IdPedido = IP.IdPedido
WHERE P.Status = 'Entregue'
GROUP BY C.Nome
ORDER BY TotalGasto DESC;
"""

# Q13. Faturamento mês a mês
# Colunas do resultado: Mes, PedidosEntregues, Faturamento
Q13 = """
SELECT
    MONTH(P.DataPedido) AS Mes,
    COUNT(DISTINCT P.IdPedido) AS TotalPedidos,
    SUM(IP.Quantidade * IP.PrecoUnitario) AS Faturamento
FROM Pedidos P
INNER JOIN ItensPedido IP
    ON P.IdPedido = IP.IdPedido
WHERE P.Status = 'Entregue'
GROUP BY MONTH(P.DataPedido)
ORDER BY Mes;
"""

# Q14. Entregador do trimestre
# Colunas do resultado: Nome, Entregas, NotaMedia
Q14 = """
SELECT
    E.Nome AS Entregador,
    COUNT(P.IdPedido) AS TotalEntregas,
    AVG(CAST(P.Avaliacao AS DECIMAL(4,2))) AS NotaMedia
FROM Entregadores E
INNER JOIN Pedidos P
    ON E.IdEntregador = P.IdEntregador
WHERE P.Status = 'Entregue'
GROUP BY E.Nome
HAVING COUNT(P.IdPedido) >= 4
    AND AVG(CAST(P.Avaliacao AS DECIMAL(4,2))) >= 4
ORDER BY TotalEntregas DESC;

"""

# Q15. Valor total dos pedidos de março
# Colunas do resultado: IdPedido, Nome, ValorProdutos, TaxaEntrega, ValorTotal
Q15 = """
SELECT
    P.IdPedido,
    C.Nome AS Cliente,
    SUM(IP.Quantidade * IP.PrecoUnitario)
        + P.TaxaEntrega AS ValorTotal
FROM Pedidos P
INNER JOIN Clientes C
    ON P.IdCliente = C.IdCliente
INNER JOIN ItensPedido IP
    ON P.IdPedido = IP.IdPedido
WHERE P.Status = 'Entregue'
    AND P.DataPedido BETWEEN '2026-03-01' AND '2026-03-31'
GROUP BY
    P.IdPedido,
    C.Nome,
    P.TaxaEntrega
ORDER BY ValorTotal DESC;
"""

# Q16. Clientes sem nenhum pedido
# Colunas do resultado: Nome, Bairro, DataCadastro
Q16 = """
SELECT
    C.Nome AS Cliente,
    C.Bairro
FROM Clientes C
LEFT JOIN Pedidos P
    ON C.IdCliente = P.IdCliente
WHERE P.IdPedido IS NULL;
"""

# Q17. Produto que nunca foi vendido
# Colunas do resultado: NomeProduto, Categoria, Preco
Q17 = """
SELECT
    PR.NomeProduto,
    PR.Categoria,
    PR.Preco
FROM Produtos PR
LEFT JOIN ItensPedido IP
    ON PR.IdProduto = IP.IdProduto
WHERE IP.IdPedido IS NULL;
"""