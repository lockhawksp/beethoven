import 'dart:convert';
import 'dart:html';
import 'dart:js';


DivElement questionsDiv = querySelector('#questions');


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


void addQuestion(Event e) {
  DivElement questionDiv = new DivElement();
  questionDiv.classes.add('form-group');

  // Question input
  InputElement questionInput = new InputElement();
  questionInput.classes.add('form-control question-input');

  // Label
  LabelElement label = new LabelElement();
  label.text = 'Question';

  // Delete button
  ButtonElement deleteButton = new ButtonElement();
  deleteButton.text = 'Delete';
  deleteButton.classes.add('btn btn-danger btn-xs pull-right');

  questionDiv.children..add(label)
                      ..add(deleteButton)
                      ..add(questionInput);

  questionsDiv.children.add(questionDiv);
}


List collectQuestions() {
  List<String> questions = [];
  List questionInputs = querySelectorAll('input.question-input');
  for (InputElement questionInput in questionInputs) {
    String question = questionInput.value;
    if (question != '') {
      questions.add(questionInput.value);
    }
  }
  return questions;
}

void submitQuestions(Event e) {
  e.preventDefault();

  List questions = collectQuestions();
  String data = JSON.encode(collectQuestions());

  InputElement questionsInput = querySelector('#questions-input');
  questionsInput.value = data;

  FormElement form = querySelector('#questions-form');
  form.submit();
}


void main() {
  querySelector('#add-question').onClick.listen(addQuestion);
  querySelector('#submit-questions').onClick.listen(submitQuestions);
}
