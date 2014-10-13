import 'dart:convert';
import 'dart:html';
import 'dart:js';


Map _context = null;

// Map between id attribute of answer input element and id of question which
// the input element is for
Map answerInputIds = {};

Map questionIdToAnswerId = {};

Map questionIdToAnswer = {};

List quizQuestions;


getContext(String key) {
  if (_context == null) {
    _context = JSON.decode(context['context']);
  }
  return _context[key];
}


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


void fetchQuiz(String url) {
  var request = HttpRequest.getString(url).then(quizFetched);
}


void quizFetched(String responseText) {
  Map data = JSON.decode(responseText);

  String articleDetailsUrl = data['article'];
  fetchArticle(articleDetailsUrl);

  quizQuestions = data['questions'];
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


void takeQuiz(Event e) {
  fetchAnswerSheet(getContext('answer_sheet_details_url'));
  makeArticleColumnHalfWidth();
  (e.target as ButtonElement).style.visibility = 'hidden';
}


void fetchAnswerSheet(String url) {
  var request = HttpRequest.getString(url).then(answerSheetFetched);
}


void answerSheetFetched(String responseText) {
  Map data = JSON.decode(responseText);

  for (Map answer in data['answers']) {
    questionIdToAnswer[answer['question']] = answer['answer'];
    questionIdToAnswerId[answer['question']] = answer['id'];
  }

  showQuestions();
}


void makeArticleColumnHalfWidth() {
  querySelector('#article-column').classes = ['col-sm-6'];
}


void showQuestions() {
  HeadingElement panelTitle = new HeadingElement.h3();
  panelTitle.text = 'Questions';

  DivElement panelHeading = new DivElement();
  panelHeading.classes.add('panel-heading');
  panelHeading.children.add(panelTitle);

  DivElement panelBody = new DivElement();
  panelBody.classes.add('panel-body');
  panelBody.children.add(questionsDataToView(quizQuestions));

  DivElement questionPanel = new DivElement();
  questionPanel.classes.add('panel panel-default');
  questionPanel.children..add(panelHeading)
                        ..add(panelBody);

  DivElement questionColumn = new DivElement();
  questionColumn.classes.add('col-sm-6');
  questionColumn.children.add(questionPanel);

  // Dart does not have insertAfter
  querySelector('#article-column').insertAdjacentElement('afterend', questionColumn);
}


String getAnswerInputId(int id) {
  return 'answer-for-question-$id';
}


Element questionDataToView(Map data) {
  int id = data['id'];
  int seq = data['sequence'];
  String question = data['question'];
  String answer = questionIdToAnswer[id];

  DivElement questionDiv = new DivElement();
  questionDiv.classes.add('form-group');

  // Input for answer
  String answerId = getAnswerInputId(id);
  InputElement answerInput = new InputElement();
  answerInput.classes.add('form-control answer-input');
  answerInput.id = answerId;
  answerInput.value = answer;
  answerInput.attributes['data-question-id'] = id.toString();

  // Label
  LabelElement label = new LabelElement();
  label.htmlFor = answerId;
  label.text = '$seq. $question';

  questionDiv.children..add(label)
                      ..add(answerInput);

  return questionDiv;
}


DivElement questionsDataToView(List questions) {
  DivElement questionsDiv = new DivElement();
  questionsDiv.id = 'questions';

  for (Map data in questions) {
    questionsDiv.children.add(questionDataToView(data));
    int id = data['id'];
    answerInputIds[getAnswerInputId(id)] = id;
  }

  ButtonElement submitButton = new ButtonElement();
  submitButton.type = 'submit';
  submitButton.classes.add('btn btn-success');
  submitButton.id = 'submit-answers';
  submitButton.text = 'Submit answers';
  submitButton.onClick.listen(submitAnswers);
  questionsDiv.children.add(submitButton);

  return questionsDiv;
}


List collectAnswers() {
  List answers = [];
  for (String answerId in answerInputIds.keys) {
    int questionId = answerInputIds[answerId];
    Map answer = {
        'id': questionIdToAnswerId[questionId],
        'answer': (querySelector('#$answerId') as InputElement).value
    };
    answers.add(answer);
  }
  return answers;
}


void submitAnswers(Event e) {
  e.preventDefault();
  String data = JSON.encode({'answers': collectAnswers()});

  HttpRequest request = new HttpRequest();
  request.onReadyStateChange.listen((_) {
    Map data = JSON.decode(request.responseText);

    if (data.containsKey('msg') && data['msg'] == 'answers saved.') {
      window.location.assign(data['next']);
    }
  });
  String url = getContext('submit_answers_url');
  request.open('POST', url);
  request.setRequestHeader('X-CSRFToken', cookiesToMap()['csrftoken']);
  request.send(data);
}


void main() {
  fetchQuiz(getContext('quiz_details_url'));
  querySelector('#take-quiz').onClick.listen(takeQuiz);
}
