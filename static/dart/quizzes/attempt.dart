import 'dart:convert';
import 'dart:html';
import 'dart:js';


Map getContext() {
  Map data = JSON.decode(context['context']);
  return data;
}


void fetchArticle(String url) {
  var request = HttpRequest.getString(url).then(renderArticle);
}


void renderArticle(String responseText) {
  Map data = JSON.decode(responseText);
  String title = data['title'];
  String content = data['content'];

  // Render article title
  querySelector('#article-title').text = title;

  // Render article content
  List paragraphs = content.split(new RegExp(r'\n'));
  DivElement articleContentDiv = querySelector('#article-content') as DivElement;
  for (String p in paragraphs) {
    ParagraphElement paragraph = new ParagraphElement();
    paragraph.text = p;
    articleContentDiv.children.add(paragraph);
  }
}


void fetchQuiz(String url) {
  var request = HttpRequest.getString(url).then(renderQuiz);
}


Element questionDataToView(Map data) {
  int id = data['id'];
  String question = data['question'];
  int seq = data['sequence'];

  DivElement questionDiv = new DivElement();
  questionDiv.classes.add('form-group');

  // Input for answer
  String answerId = 'question-$id';
  InputElement answerInput = new InputElement();
  answerInput.classes.add('form-control');
  answerInput.id = answerId;

  // Label
  LabelElement label = new LabelElement();
  label.htmlFor = answerId;
  label.text = '$seq. $question';

  questionDiv.children..add(label)
                      ..add(answerInput);

  return questionDiv;
}


void renderQuestions(List questions) {
  DivElement questionsDiv = querySelector('#questions') as DivElement;
  for (Map data in questions) {
    questionsDiv.children.add(questionDataToView(data));
  }

  ButtonElement submitButton = new ButtonElement();
  submitButton.type = 'submit';
  submitButton.classes.add('btn btn-success');
  submitButton.id = 'submit-answers';
  submitButton.text = 'Submit answers';

  questionsDiv.children.add(submitButton);
}


void renderQuiz(responseText) {
  Map data = JSON.decode(responseText);
  String articleDetailsUrl = data['article'];
  List questions = data['questions'];

  fetchArticle(articleDetailsUrl);
  renderQuestions(questions);
}


void main() {
  Map context = getContext();
  fetchQuiz(context['quiz_details_url']);
}
