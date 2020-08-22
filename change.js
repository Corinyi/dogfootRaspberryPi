
// header라는 id를 가지고 있는 <h1> 태그를 찾아 변수에 저장합니다.
var element = document.getElementById("h1");

// 요소의 콘텐츠를 변경합니다.
element.innerText = "Hello World!";

// 요소의 콘텐츠를 출력합니다.
document.write(element.innerText);