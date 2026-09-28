-- A equipe de Product Marketing quer mapear a distribuição dos jogos na base para entender 
-- o catálogo disponível. Antes de enviarmos os dados para a análise avançada de engajamento no Python, 
-- o SQL será responsável por validar a qualidade dos registros, filtrar inconsistências e gerar 
-- uma visão geral das categorias e métricas agregadas.

select * from tabela_kaggle;

with Jogos_Tratados as (
	select 
	AppID as Nome_Jogo,
    Genres as Generos,
    Price as Preço,
    `Average playtime forever` as Tempo_De_Jogo,
    Positive as Avaliação_Positiva,
    (Positive + Negative) as Total_Avaliação,
    case
		when price = 0 then 'Gratuito'
        else 'Pago'
	end as Categoria_Jogos,
    case
		when Genres like '%,%' then 'Hibrido'
        else 'Unico'
    end as Categoria_Generos
from tabela_kaggle
where AppID is not null 
and Genres is not null
and (Positive + Negative) > 0
)
select 
	Categoria_Jogos,
	count(Nome_Jogo) as Qtd_Jogos,
    round(avg(Tempo_De_Jogo), 0) as Tempo_Medio_Geral,
    round((sum(Avaliação_Positiva) / sum(Total_Avaliação)) * 100, 2) as Taxa_Aprovação_Pct
from Jogos_Tratados
group by Categoria_Jogos;