import 'dart:html';
import 'dart:js';


String getDeadline() {
  JsObject deadlineDate = context['deadlineDatePicker'].callMethod('get', ['select']);
  JsObject deadlineTime = context['deadlineTimePicker'].callMethod('get', ['select']);

  if (deadlineDate != null && deadlineTime != null) {
    int year = deadlineDate['year'];
    int month = deadlineDate['month'] + 1;
    int date = deadlineDate['date'];
    int hour = deadlineTime['hour'];
    int minute = deadlineTime['mins'];
    return new DateTime(year, month, date, hour, minute).toUtc().toIso8601String();
  }

  else {
    return '';
  }
}


void createQuiz(Event e) {
  e.preventDefault();

  String deadline = getDeadline();
  (querySelector('#deadline') as InputElement).value = deadline;

  FormElement form = querySelector('#quiz');
  form.submit();
}


void main() {
  querySelector('#create-quiz').onClick.listen(createQuiz);
}
