import polars as pl
import os

class polars_partitions:
    def __init__(self):
        pass
        
    # Создание TOC - Table Of Contents
    def wr_toc(self, df, columns, output_path):  
        prqt = pl.DataFrame(df[columns].unique())

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        prqt.write_parquet(f'{output_path}/toc.parquet')
        print(f'{output_path}/toc.parquet - записан')
        print(f'Создано {len(prqt)} партиций')
        
    # Запись партиций или одного паркета
    def wr_partition(self, df, columns, output_path):
        df.write_parquet(
            output_path,
            use_pyarrow=True,
            pyarrow_options={"partition_cols": columns}
        )
        self.wr_toc(df, columns, output_path)
    
    # Чтение и поиск в TOC
    def rd_toc(self, output_path, filters=None, btwn=None):  
        df_toc = pl.read_parquet(f'{output_path}/toc.parquet')
        
        # Если фильтр по партициям был указан пройтись по каждому и вернуть только те значения,
        # которые есть в TOC
        if filters is not None and bool(filters):
            for index in range(df_toc.width):  
                clmn_nm = df_toc.columns[index]
                
                if clmn_nm in filters:
                    if btwn == clmn_nm:
                        df_toc = df_toc.filter(pl.col(clmn_nm).is_between(filters[clmn_nm][0],filters[clmn_nm][1]))
                    else:
                        df_toc = df_toc.filter(pl.col(clmn_nm).is_in(filters[clmn_nm]))
        
        return df_toc
        
    # Чтение партиций на основании toc
    def rd_partition(self, output_path, columns='*', filters=None, btwn=None):
        dir_parquet = self.rd_toc(output_path, filters, btwn)
        
        if filters is not None and bool(filters):
            try:
                # Оставляем столбец, который не указали в фильтре при вызове и проставляем *, 
                # Делаем датафрейм уникальным по всем полям
                for clmn in list(set(dir_parquet.columns) - set(list(filters.keys()))):
                    dir_parquet = dir_parquet.with_columns(pl.lit('*').alias(clmn)).unique() 

                # Проставляем каджой записи фильтр по шаблону "поле=партиция"
                for clmn in list(filters.keys()):
                    dir_parquet = dir_parquet.with_columns((clmn + '=' + pl.col(clmn)).alias(clmn))

                # Объединяем все и оставляем только столбец path
                dir_parquet = dir_parquet.with_columns(
                    pl.concat_str([pl.col(i) for i in dir_parquet.columns],
                                  separator='/',
                                 ).alias('path')).select(pl.col('path'))
                
                # Читам все партиции удовлетворяющие условиям
                with pl.StringCache():
                    for index in range(dir_parquet.width):
                        dfs = [pl.scan_parquet(f'{output_path}/{dir}/*').select(pl.col(columns))for dir in dir_parquet['path']]
                    return pl.concat(dfs)
                
            # Если в оглавлении не нашлось ничего, что подходит под условия поиска, вернуть пустой массив
            except ValueError:
                return pl.DataFrame()
            
            except Exception:
                raise ValueError(f'Партиции по колонке {clmn} - Не существует')

        else:  # Загрузка всех паркетов
            path = '/*'.join(['/*' for _ in range(dir_parquet.width)])
            with pl.StringCache():
                return pl.scan_parquet(f'{output_path}{path}').select(pl.col(columns))          
