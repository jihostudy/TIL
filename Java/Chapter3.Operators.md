자바는 초기화하지 않은 변수를 사용하면, 컴파일 에러가 발생한다.

```java
int a;
int b = 1;
System.out.println(a + b); // ❌ 컴파일 에러
```

### Primitive Type (기본 타입 / 원시 타입)

총 8가지 원시 타입을 제공한다.

- 각 타입에 따라 메모리 사용 크기와 저장되는 값의 범위가 다르다.
- char 타입을 제외하고, -2^(n-1) ~ 2^(n-1) -1 의 값을 가질 수 있다. (char 타입은 0이상의 값을 가질 수 있다).
  - n: bit수

| 타입                          | 바이트 크기 | 값의 범위                                                      | 설명                                       |
| ----------------------------- | ----------- | -------------------------------------------------------------- | ------------------------------------------ |
| `byte`                        | 1           | -128 to 127                                                    | 매우 작은 정수 저장용.                     |
| 네트워크 데이터 처리에 유용   |
| `short`                       | 2           | -32,768 to 32,767                                              | 작은 정수 저장용.                          |
| `byte` 보다 큰 범위 제공      |
| `int`                         | 4           | -2,147,483,648 to 2,147,483,647                                | 일반적으로 사용되는 정수 저장용.           |
| 가장 자주 사용됨              |
| `long`                        | 8           | -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807        | 매우 큰 정수 저장용                        |
| `float`                       | 4           | 대략 ±3.40282347E+38F (6-7 significant decimal digits)         | 실수 저장용. 부동소수점 연산에 사용        |
| `double`                      | 8           | 대략 ±1.79769313486231570E+308 (15 significant decimal digits) | 더 큰 실수 저장용.                         |
| 정밀한 부동소수점 연산에 사용 |
| `char`                        | 2           | '\u0000' to '\uffff' (0 to 65,535)                             | 단일 문자 저장용. 유니코드 문자 표현 가능  |
| `boolean`                     | 1 bit       | true, false                                                    | 논리값 저장용. 조건문과 제어문에 주로 사용 |

[long 타입 사용시 주의점]

기본적으로 자바는 정수 리터럴을 `int` 타입으로 간주한다.

따라서, 다음과 같이 `long`으로 선언했음에도 `int` 범위를 넘어서는 경우, 컴파일 에러를 발생시킨다.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/eeab3f36-a8f3-42ff-a354-cbb7f6130b3a/9468b1ee-e4f7-4128-9df1-c62d3d52c6a6/image.png)

따라서, 컴파일러에게 `long` 타입임을 알려주기 위해 숫자 뒤에 `L` 을 붙여야 한다.

```java
long lo = 2147483648L;
```

[float 타입 사용시 주의점]

기본적으로 자바는 실수 리터럴을 double 타입으로 해석하기 때문에, double 타입 변수에 저장해야 한다.

실수 리터럴을 float 타입 변수에 저장하면 컴파일 에러가 발생한다.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/eeab3f36-a8f3-42ff-a354-cbb7f6130b3a/9701d01c-089a-4c1f-8834-0ba94d3fa5d2/image.png)

따라서, float 자료형을 사용하고 싶으면, 소문자 f나 대문자 F를 붙여주어야 한다.

```java
float var = 3.14f;
```

[char 타입]

char 타입의 문자 인코딩(사용자가 입력한 문자나 기호들을 컴퓨터가 이용할 수 있는 신호로 만드는 것)은 유니코드를 사용하여 변환하고 이를 저장다.

- 아스키코드 (0 ~ 127)에서 확장되어, 다양한 언어를 지원하는 것이 유니코드(2byte)이다.

[String 클래스]

char를 사용하여 문자를 선언할 때는 작음따음표 `(’)` 를 사용하여 저장하지만, 문자열을 사용할 때는 큰따음표 (”)를 사용하며, char 타입에 저장할 . 수없다. (컴파일 에러 발생)

따라서, 문자열을 사용하고 싶으면 String 클래스를 사용해야 한다

```java
char str = "123";   ❌
String str = "123"; ✅
```

### 입출력 시스템

System.out은 시스템의 표준 출력 장치를 말한다.

- out이 표준 출력 장치라면, in은 표준 입력 장치를 의미한다.

System.out.

- `println` : 출력 + 행 바꾸기
- `print` : 출력
- `printf(”형식문자열”, 값1, 값2 … )` : c언어와 같이 출력
  - 형식 문자열에서는 flags를 사용하여 width, precision을 사용가능

`System.in.read()` 를 사용하여 입력을 받으면, 문자 기준으로 입력을 받기 때문에 Carriage Return과 Line Fead(윈도우의 경우)도 입력으로 처리된다.

따라서, 입력은 **Scanner 클래스**를 사용한다.

```java
Scanner scanner = new Scanner(System.in);
String inputData = scanner.nextline();
```

- Scanner로 입력받은 데이터는 String에 저장된다.
- Scanner를 `import`해서 사용한다.
  - `java.util`은 JDK에서 제공하는 기능이다.
  ```java
  import java.util.Scanner;

  public class RunStatementExample {
      public static void main(String[] args) throws Exception {
          Scanner sc = new Scanner(System.in);

          String keycode;

          while(true) {
              keycode = sc.nextLine();
              System.out.println("Keycode: " + keycode);
              if(keycode.equals("exit")) break;
          }
      }
  }
  ```
  > 참조 타입인 String 변수를 비교할 때에는 `equals()` 메소드를 사용한다.
