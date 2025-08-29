## reduce 함수 사용법

> 형태: `array.reduce(콜백함수, 초기값);`

콜백함수 인자

- 자바스크립트에서 자동 인자를 제공하며 총 4가지 인자를 제공한다
  - accumulator: 이전 요소를 상대로 콜백 함수를 실행한 결과 (누적자)
  - currentValue: 현재 요소의 값
  - currentIndex: 현재 요소의 인덱스
  - array: `reduce()` 메서드를 호출하는 배열

보통 처음 2개의 요소를 자주 사용한다.

reduce 메소드를 사용하면 다음과 같은 장점이 있다.

- `let` 대신 `const`를 값에 지정하여 더욱 견고한 코딩이 가능하다.
- 배열의 요소를 순회할때 더 유용하다.

기본 예제

1. 누적 계산

```jsx
const numbers = [2, 4, 3, 1];
const sum = numbers.reduce((acc, num) => acc + num, 0);
console.log(sum); // 10
```

1. 최대값, 최소값 구하기

```jsx
const numbers = [2, 4, 3, 1];
const max = numbers.reduce((max, num) => (max < num ? num : max));
const min = numbers.reduce((min, num) => (min > num ? num : min));
```

Q) `Math.max`, `Math.min` 내장 메소드를 사용하면 더 편리하게 개발할 수 있지 않나요?

A) Math.max 메소드의 모든 인자는 함수의 인자로 전달되어 스택에 저장된다. 따라서 ,인자의 값 (배열 요소의 개수)이 너무 많아지면 스택 오버플로우가 발생할 수 있다.

`Math.min(...arrayA)`는 **스프레드 연산자(`...`)를 사용**하여 배열의 모든 요소를 개별 인자로 전달합니다.

즉, 아래와 같이 동작합니다.

```jsx
Math.min(arrayA[0], arrayA[1], arrayA[2], ... , arrayA[N-1]);
```

**"Maximum call stack size exceeded"** 또는 **"Too many arguments"** 같은 런타임 오류가 발생할 수 있다.

1. 개수 세기

[기존]

```jsx
const fruits = ["apple", "banana", "apple", "orange", "banana", "apple"];
let fruitCounts = {};
for (const friut of fruits) {
  if (!fruitCounts[fruit]) fruitCounts[fruit] = 1;
  else fruitCounts[fruit] += 1;
}
```

reduce 함수 이용방법

```jsx
const fruits = ["apple", "banana", "apple", "orange", "banana", "apple"];
const fruitCounts = fruits.reduce((counter, fruit) => {
  if (fruit in counter) {
    counter[fruit]++;
  } else {
    counter[fruit] = 1;
  }
  return counter;
}, {});
```

ES6 도입 이후 방법

```jsx
const fruits = ["apple", "banana", "apple", "orange", "banana", "apple"];
const fruitCounts = fruits.reduce(
  (counter, fruit) => ({
    ...counter,
    [fruit]: fruit in counter ? counter[fruit] + 1 : 1,
  }),
  {}
);
```

### 타입스크립트 사용 방법

타입 오류를 해결하려면 `reduce<결과 타입>`의 형태로 결과 값의 타입을 명시적으로 표시해줘야 합니다.

ex) 명시적으로 언급하는 방법

```jsx
const fruits = ["apple", "banana", "apple", "orange", "banana", "apple"];
const fruitCounts = fruits.reduce<{ [key: string]: number }>(
  (counter, fruit) => {
    counter[fruit] = fruit in counter ? counter[fruit] + 1 : 1;
    return counter;
  },
  {}
);
```

ex) 타입스크립트 유틸리티 함수를 이용하는 방법

```jsx
const fruits = ["apple", "banana", "apple", "orange", "banana", "apple"];
const fruitCounts = fruits.reduce<Record<string,number>>(
  (counter, fruit) => {
    counter[fruit] = fruit in counter ? counter[fruit] + 1 : 1;
    return counter;
  },
  {}
);
```
