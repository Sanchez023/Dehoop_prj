WITH
  O_ODS AS (
    SELECT
      *
    FROM
      ODS_HBCORE_{{TABLENAME}}
    WHERE
      createtime IN (
        SELECT
          DISTINCT SUBSTRING(createtime, 1, 7) as createtime
        FROM
          STG_HBCORE_{{TABLENAME}}
      )
  ) 
 INSERT OVERWRITE ODS_HBCORE_{{TABLENAME}} PARTITION(DS)
SELECT
  ODS.*
FROM
  O_ODS ODS
  LEFT JOIN STG_HBCORE_{{TABLENAME}} STG ON ODS.PROPOSALNO = STG.PROPOSALNO
WHERE
  STG.PROPOSALNO IS NULL
UNION ALL
SELECT
  STG.*,
  SUBSTRING(STG.createtime, 1, 7) AS DS
FROM
  STG_HBCORE_{{TABLENAME}} STG