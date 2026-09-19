SELECT class, COUNT(*) AS count
FROM detection_events
GROUP BY class
ORDER BY count DESC;
