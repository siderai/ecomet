WITH hourly_max AS (
    SELECT
        phrase,
        toHour(dt) AS hour,
        max(views) AS max_views_in_hour
    FROM phrases_views
    WHERE
        campaign_id = 1111111
        AND toDate(dt) = '2025-01-01' 
    GROUP BY phrase, hour
),
hourly_incremental AS (
    SELECT
        phrase,
        hour,
        max_views_in_hour - coalesce(
            lagInFrame(max_views_in_hour, 1) OVER (
                PARTITION BY phrase
                ORDER BY hour ASC
                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
            ),
            0
        ) AS hourly_views
    FROM hourly_max
)
SELECT
    phrase,
    groupArray((hour, hourly_views)) AS views_by_hour
FROM (
    SELECT
        phrase,
        hour,
        hourly_views
    FROM hourly_incremental
    WHERE hourly_views > 0
    ORDER BY phrase ASC, hour DESC
)
GROUP BY phrase
ORDER BY phrase ASC;
