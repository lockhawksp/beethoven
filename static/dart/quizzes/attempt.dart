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


void main() {
  Map context = getContext();
  fetchArticle(context['article_details_url']);
}
