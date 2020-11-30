package com.amazonaws.rhythmCloud;

public class Constants {
  public enum HIT_TYPES {
    USER,
    SYSTEM
  }

  public static final String DATABASE_NAME = "rhythm_cloud";
  public static final String TABLE_NAME = "rhythm-cloud-hits";
  public static final String GET_SCORE_QUERY_TEMPLATE =
      "WITH system AS( "
          + "  SELECT time, drum, ROW_NUMBER() OVER(PARTITION BY session_id ORDER BY time ASC) as sequence_id FROM \""
          + DATABASE_NAME
          + "\".\""
          + TABLE_NAME
          + "\" "
          + "  WHERE session_id = '%s' AND hit_type = '"
          + HIT_TYPES.SYSTEM.name().toLowerCase()
          + "' AND measure_name='drum' AND drum <> 'metronome'"
          + "), "
          + "user AS( "
          + "  SELECT time, drum, ROW_NUMBER() OVER(PARTITION BY session_id ORDER BY time ASC) as sequence_id FROM \""
          + DATABASE_NAME
          + "\".\""
          + TABLE_NAME
          + "\" "
          + "  WHERE session_id = '%s' AND hit_type = '"
          + HIT_TYPES.USER.name().toLowerCase()
          + "' AND measure_name='drum' "
          + "), "
          + "joined AS( "
          + "SELECT system.time AS a, user.time AS b, system.drum AS x, user.drum AS y, "
          + "if(system.drum = user.drum, 1, 0) AS score FROM system INNER JOIN user "
          + "ON(system.sequence_id = user.sequence_id))"
          + "SELECT SUM(score) AS score, ((100 * SUM(score))/COUNT(a)) AS pct_score FROM joined";
  ;
}
