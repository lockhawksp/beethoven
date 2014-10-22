import 'dart:convert';
import 'dart:html';
import 'dart:js';


Map cookiesToMap() {
  Map cookies = {};
  List items = document.cookie.split(new RegExp(r'; '));
  for (String item in items) {
    int i = item.indexOf('=');
    String key = item.substring(0, i);
    String value = item.substring(i+1, item.length);
    cookies[key] = value;
  }
  return cookies;
}


List collectSolutions() {
  List<Map> solutions = [];
  querySelectorAll('.solution-input').forEach((InputElement e) {
    Map solution = {
      'question_id': int.parse(e.attributes['data-question-id']),
      'solution': e.value
    };
    solutions.add(solution);
  });

  return solutions;
}


void submitSolutions(Event e) {
  e.preventDefault();

  List solutions = collectSolutions();

  HttpRequest request = new HttpRequest();
  request.onReadyStateChange.listen((_) {
    if (request.readyState == HttpRequest.DONE &&
        (request.status == 200 || request.status == 0)) {
      Map data = JSON.decode(request.responseText);

      if (data.containsKey('msg') && data['msg'] == 'solutions saved.') {
        window.location.assign(data['next']);
      }
    }
  });

  String url = context['submit_solution_url'];
  request.open('POST', url);
  request.setRequestHeader('X-CSRFToken', cookiesToMap()['csrftoken']);
  request.send(JSON.encode({'solutions': solutions}));
}


void main() {
  querySelector('#submit-solutions').onClick.listen(submitSolutions);
}
