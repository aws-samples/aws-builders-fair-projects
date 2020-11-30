package com.amazonaws.rhythmCloud;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.LambdaLogger;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.APIGatewayProxyRequestEvent;
import com.amazonaws.services.lambda.runtime.events.APIGatewayProxyResponseEvent;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.timestreamquery.TimestreamQueryClient;
import software.amazon.awssdk.services.timestreamquery.model.*;
import software.amazon.awssdk.services.timestreamquery.paginators.QueryIterable;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/** Handler for requests to Lambda function. */
public class App
    implements RequestHandler<APIGatewayProxyRequestEvent, APIGatewayProxyResponseEvent> {
  private final TimestreamQueryClient timestreamQueryClient = buildQueryClient();
  Gson gson = new GsonBuilder().setPrettyPrinting().create();

  public APIGatewayProxyResponseEvent handleRequest(
      final APIGatewayProxyRequestEvent input, final Context context) {
    String sessionId = "c15f9236-c945-4139-91a9-7c952ecb67b3";
    LambdaLogger logger = context.getLogger();
    Map<String, String> headers = new HashMap<>();
    headers.put("Content-Type", "application/json");
    headers.put("X-Custom-Header", "application/json");
    headers.put("Access-Control-Allow-Headers", "Content-Type");
    headers.put("Access-Control-Allow-Origin", "*");
    headers.put("Access-Control-Allow-Methods", "OPTIONS,POST,GET");

    if (input != null
        && input.getQueryStringParameters() != null
        && input.getQueryStringParameters().containsKey("sessionid")) {
      logger.log("Session Id: " + input.getQueryStringParameters().get("sessionid"));
      sessionId = input.getQueryStringParameters().get("sessionid");
    } else {
      logger.log(
          "Using the default session id. Could not find the session id parameter in the query string");
    }

    APIGatewayProxyResponseEvent response = new APIGatewayProxyResponseEvent().withHeaders(headers);
    try {
      String query = String.format(Constants.GET_SCORE_QUERY_TEMPLATE, sessionId, sessionId);
      logger.log(query);
      List<String> results = runQuery(query);
      String output = gson.toJson(results);
      return response.withStatusCode(200).withBody(output);
    } catch (Exception e) {
      logger.log(e.toString());
      return response
          .withBody(String.format("{\"exception\": \"%s\"}", e.getMessage()))
          .withStatusCode(500);
    }
  }

  private List<String> runQuery(String query) {
    List<String> output = new ArrayList<>();
    QueryRequest request = QueryRequest.builder().queryString(query).build();
    final QueryIterable queryResponseIterator = timestreamQueryClient.queryPaginator(request);
    for (QueryResponse queryResponse : queryResponseIterator) {
      List<ColumnInfo> columnInfo = queryResponse.columnInfo();
      List<Row> rows = queryResponse.rows();
      // iterate every row
      for (Row row : rows) {
        output.add(parseRow(columnInfo, row));
      }
    }
    return output;
  }

  private String parseRow(List<ColumnInfo> columnInfo, Row row) {
    List<Datum> data = row.data();
    List<String> rowOutput = new ArrayList<>();
    // iterate every column per row
    for (int j = 0; j < data.size(); j++) {
      ColumnInfo info = columnInfo.get(j);
      Datum datum = data.get(j);
      rowOutput.add(parseDatum(info, datum));
    }
    return String.format(
        "{%s}", rowOutput.stream().map(Object::toString).collect(Collectors.joining(",")));
  }

  private String parseDatum(ColumnInfo info, Datum datum) {
    if (datum.nullValue() != null && datum.nullValue()) {
      return info.name() + "=" + "NULL";
    }
    Type columnType = info.type();
    // If the column is of TimeSeries Type
    if (columnType.timeSeriesMeasureValueColumnInfo() != null) {
      return parseTimeSeries(info, datum);
    }
    // If the column is of Array Type
    else if (columnType.arrayColumnInfo() != null) {
      List<Datum> arrayValues = datum.arrayValue();
      return info.name() + "=" + parseArray(info.type().arrayColumnInfo(), arrayValues);
    }
    // If the column is of Row Type
    else if (columnType.rowColumnInfo() != null && columnType.rowColumnInfo().size() > 0) {
      List<ColumnInfo> rowColumnInfo = info.type().rowColumnInfo();
      Row rowValues = datum.rowValue();
      return parseRow(rowColumnInfo, rowValues);
    }
    // If the column is of Scalar Type
    else {
      return parseScalarType(info, datum);
    }
  }

  private String parseTimeSeries(ColumnInfo info, Datum datum) {
    List<String> timeSeriesOutput = new ArrayList<>();
    for (TimeSeriesDataPoint dataPoint : datum.timeSeriesValue()) {
      timeSeriesOutput.add(
          "{time="
              + dataPoint.time()
              + ", value="
              + parseDatum(info.type().timeSeriesMeasureValueColumnInfo(), dataPoint.value())
              + "}");
    }
    return String.format(
        "[%s]", timeSeriesOutput.stream().map(Object::toString).collect(Collectors.joining(",")));
  }

  private String parseScalarType(ColumnInfo info, Datum datum) {
    return parseColumnName(info) + datum.scalarValue();
  }

  private String parseColumnName(ColumnInfo info) {
    return info.name() == null ? "" : info.name() + "=";
  }

  private String parseArray(ColumnInfo arrayColumnInfo, List<Datum> arrayValues) {
    List<String> arrayOutput = new ArrayList<>();
    for (Datum datum : arrayValues) {
      arrayOutput.add(parseDatum(arrayColumnInfo, datum));
    }
    return String.format(
        "[%s]", arrayOutput.stream().map(Object::toString).collect(Collectors.joining(",")));
  }

  private static TimestreamQueryClient buildQueryClient() {
    return TimestreamQueryClient.builder().region(Region.US_EAST_1).build();
  }
}
