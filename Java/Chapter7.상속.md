## 상속

- `extends` 키워드를 통해 상속 받을 수 있다.
- 부모의 인스턴스, 메소드를 사용할 수 있다.
- `super()` 는 부모의 생성자 함수를 사용하는 것이다.
  - 항상 생성자의 처음에 써주어야 함.
  - 사용하지 않을 경우, 부모 클래스의 생성자 함수에 빈 값을 넣어서 호출된다.

주의

- 자바는 여러 개의 부모 클래스를 상속할 수 없다 (다중 상속을 허용하지 않는다)
  ```java
  class A extends B, C {} // ❌
  ```
- 부모 클래스에서 `private` 접근 제어자를 가지는 필드와 메소드는 상속에서 제외된다.
  ```java
  class Parent {
  	private String name;

  	public String getName() {
  		return this.name;
  	}
  }

  class Child extends Parent {

  	public void printName () {
  		System.out.println(this.name); // ❌ Error (private 값에 접근할 수 없음)
  		System.out.println(this.getName()); // ✅
  	}
  }
  ```

### 메소드 오버로딩 vs 오버라이딩

- 오버로딩 (Overloading)
  하나의 클래스 내부에서 메소드를 매개변수의 타입이나 개수를 다르게 하여 여러 번 정의하는 것
  ```java
  class Animal {
      public String bark() {
          return "bark-bark";
      }

      public String bark(String voice) {
          return voice;
      }
  }
  ```
- 오버라이딩
  자식 클래스에서 부모 클래스의 메소드를 재정의하는 방법
  ```java
  public class Cat extends Animal {
     // #2. 메소드 오버라이팅
      @Override
      public String bark() {
          return "사람은 짖지 않습니다";
      }
  }
  ```

### `final` 클래스와 메소드

- `final` 클래스는 최종적인 형태로 상속할 수 없다.
- `final` 메소드는 재정의(메소드 오버라이딩)할 수 없다.

```java
public final class A {
	public final method1() {}
}

public class B extends A {   // ❌ A는 final로 선언되어서 상속할 수 없음
	public final method1() { } // ❌ final method는 상속할 수 없음. (재정의 불가능)
}
```

### 다형성

국어사전 의미: 같은 종의 생물이면서도 어떤 형태나 형질이 다양하게 나타나는 현상

→ 같은 자료형에 여러가지 타입의 데이터를 대입하여 다양한 결과를 얻어낼 수 있는 성질

만일, 상속 관계에 있다면 부모 타입으로 자식 클래스 타입을 받아 초기화 할수 있다.

- 이때, 부모 타입의 변수에 자식을 할당하는 것은 가능하나, 자식 타입의 변수에 부모를 할당하는 것을 불가능하다.
  - 이유
    아래 예시에서 smartTV로 선언된 인스턴스에서 TV를 저장하는 경우, smartTV 리모콘으로 TV를 조작하겠다는 것이랑 다른게 없다.
    그럴 경우, smartTV 리모콘의 기능을 사용하면 일반 TV에서는 오류가 발생하겠죠?
    반면, 일반 TV 리모콘으로 smartTV를 조작하는 경우, smartTV의 기능을 사용하지 못할 뿐 일반 TV와 smartTV가 같이 지니고 있는 기능(채널 이동, 볼륨 조절)은 사용가능하겠죠?

```java
// 일반적인 객체 상속
class TV {
	public method1() {
		System.out.println("origin"); // 1️⃣ 기존
	}
}

class smartTV extends TV {
	public method1() {
		System.out.println("overrided"); // 2️⃣ 오버라이딩
	}
}
```

가능한 경우

- 생성된 인스턴스는 부모의 멤버, 인스턴스만 사용가능하다
- 단, 자식에서 메소드 오버라이딩된 경우 해당 메소드로 사용가능하다

```java
TV 내티비 = new smartTV();
내티비.method1(); // 2️⃣ 사용
```

불가능한 경우

```java
smartTV 내티비 = new TV();
```

---

그렇다면 다형성은 왜 하는 것일까? → 타입을 묶을 수 있다. (필드의 다형성)

- 필드의 타입을 부모 타입으로 선언하면 다양한 자식 객체들이 저장될 수 있기 때문에 필드 사용 결과가 달라질 수 있다.

아래 왼쪽과 같이 반복되는 코드를 오른쪽 처럼 묶어서 사용할 수 있다.

만약, 자식 클래스에서 전용 메소드를 사용해야 한다면 **메소드 오버라이딩을 통해 그 요소만 다운캐스팅해주면 된다.**

```java
class Rectangle {
}

class Triangle {
}

class Circle {
}

ArrayList<Rectangle> rectangles = new ArrayList<>();
rectangles.add(new Rectangle(1,2,3,4));
rectangles.add(new Rectangle(10,20,30,40));
rectangles.forEach(each -> System.out.println(each));

ArrayList<Triangle> triangles = new ArrayList<>();
triangles.add(new Triangle(1,2,3));
triangles.add(new Triangle(10,20,30));
triangles.forEach(each -> System.out.println(each));

ArrayList<Circle> circles = new ArrayList<>();
circles.add(new Circle());
circles.add(new Circle());
circles.forEach(each -> System.out.println(each));
```

```java
class Shape {
}

class Rectangle extends Shape {
}

class Triangle extends Shape {
}

class Circle extends Shape {
}

ArrayList<Shape> shapes = new ArrayList<>();
shapes.add(new Rectangle(1,2,3,4));
shapes.add(new Rectangle(10,20,30,40));
shapes.add(new Triangle(1,2,3));
shapes.add(new Triangle(10,20,30));
shapes.add(new Circle());
shapes.add(new Circle());
shapes.forEach(each -> System.out.println(each));
```

다형성은 객체 지향의 SOLID 원칙의 OCP(Open Closed Principle), LSP(Listov Substitution Principle)과 밀접하게 관련되어 있다.

OCP : 확장에는 열려 있으며, 수정에는 닫혀 있여야 한다.

- 다형성으로 구현을 하면, 새로운 `Start extends Shape`가 생성되어도 무리 없이 개발을 진행할 수 있는 것 처럼 말이다.

LSP : 서브 타입은 부모 타입으로 언제나 교체가능해야 한다.

- 교체할 수 있다는 말은, 자식 클래스는 최소한 자신의 부모 클래스에서 가능한 행위(메소드)는 수행이 보장되어야 한다는 의미이다.
- 부모 클래스의 인스턴스를 사용하는 위치에 자식 클래스의 인스턴스를 대신 사용했을때 코드가 원래 의도대로 작동해야 한다는 의미

  - 결국 다형성 원리를 적용한다는 뜻.

- 객체 타입 확인 방법
  `boolean result = 좌항(객체) instanceof 우항(타입)`
  instanceof 연산자로 확인해보면 된다.

### 추상 클래스

추상 클래스는 일종의 설계 규격으로, 공통된 필드와 메소드를 정의한다.

- `abstract` 키워드를 붙여 사용한다.
  ```java
  public abstract class 클래스 {}
  ```
- 추상 클래스는 타클래스에서 상속만 가능하며, `new`를 통해 인스턴스를 생성할 수 없다.
- 클래스마다 정의하는 경우, 네이밍 규칙을 정할 수 있는 장점이 있다.
- abstract 키워드를 메소드에 붙여, 추상 메소드를 사용할 수 있다.
  - 추상 메소드는 함수의 선언만 해두는 방법으로, 메소드의 내용은 각 자식 클래스가 직접 선언하도록 규격만 설계해두는 방법이다.
  - 이때, 자식 클래스는 반드시 추상 메소드를 재정의해야 한다.
    ```java
    public abstract 리턴타입 메소드이름(매개변ㅅ,....);
    ```
