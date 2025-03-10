# 스프링 컨테이너

스프링 컨테이너는 애플리케이션의 설정 정보를 바탕으로 스프링 빈의 생성, 의존 관계 주입, 생명 주기 관리 등을 수행

크게 `ApplicationContext`와 `BeanFactory`로 구분된다.

- `ApplicationContext`는 `BeanFactory`의 확장된 형태로, 국제화 지원, 이벤트 발행 등 추가적인 기능을 제공한다.

### 1. BeanFactory

빈을 생성하고 의존관계를 설정하는 기능을 담당하는 가장 기본적인 IoC 컨테이너이자 클래스를 의미한다.

- `Lazy-loading` 의존성 주입을 지원
    
    실제로 객체가 필요할 때 생성된다
    

### 2. ApplicationContext

ApplicationContext는 BeanFactory를 구현하고 있어 BeanFactory의 확장된 버전이다.

- **BeanFactory**를 확장하여, **AOP, 국제화(i18n), 이벤트 시스템, 메시지 처리** 등 다양한 부가 기능을 지원한다.
- **Pre-loading 의존성 주입**을 지원한다.
    
    컨테이너 초기화 되는 시점에 싱글톤 빈을 생성하고 필요할때 컨테이너에서 빈을 반환한다.
    
- **스프링 부트** 사용 시
    - `SpringApplication.run(MySpringBootApplication.class, args)` 호출 시 내부적으로 **적절한 ApplicationContext**를 자동 생성하고 초기화합니다.

두 컨테이너 중 특별한 이유가 없다면 ApplicationContext를 사용해야 한다.

→ BeanFactory의 모든 기능을 포함하는 것은 물론이고 추가 기능들을 제공하기 때문이다.

# IoC (Inversion of Control) 제어 역전

**객체에 대한 제어 권한**이 기존의 **개발자**에서 **스프링 IoC 컨테이너**로 **역전**되는 **디자인 원리 혹은 개념**

<aside>
💡

기존의 자바 코드는 각 객체들의 흐름 (생성, 소멸)을 개발자가 직접 제어하였다.

```java
public class Student {
	private int age;
    private String name;
    
    public Student(String name, int age) {
    	this.name = name;
        this.age = age;
    }
}

// ✅ new 키워드를 사용하여 직접 객체를 생성하는 모습
Student student = new Student("Tom", 22); 
```

하지만, IoC가 적용된 경우 객체를 사용자가 직접 생성하지 않고, 객체의 생명주기 (생성부터 소멸까지)를 Spring IoC 컨테이너가 컨트롤 하도록 한다.

</aside>

# Bean

스프링 프레임워크에서 관리하는 재사용 가능한 소프트웨어 컴포넌트(객체) 이다.

<aside>
💡

자바의 이름이 자주 마시는 커피가 인도네시아 자바 섬 커피였서서 인만큼, 자바빈은 커피콩에 비유해서 만들었다고 합니다.

그러니, 이름과 개념의 연관관계에 초점을 두지 마세요!

</aside>

- IoC에 의해 생성되고 관리되는 객체를 의미한다.
- 스프링 컨테이너의 핵심 관리 대상이다.
- DI (의존성 주입)의 대상이다.

빈은 XML 설정, 어노테이션 (@Controller, @Bean), Java Config 등 다양한 방식으로 스프링 컨테이너에 정의된다.

### 사용 이유

1. 객체 관리의 효율성 증대
    
    개발자는 객체 관리에 대한 부담 없이 비즈니스 로직에 집중할 수 있다.
    
2. 컴포넌트 재사용성 및 유지보수성 향상
    
    빈은 독립적인 단위로 설계되어서 재사용성이 높고, 설정과 코드가 분리되어 유지보수가 용이하다.
    

### 사용 방법

1. `@Component` 
    
    `@Service`, `@Repository`, `@Controller`는 자동으로 빈으로 등록된다.
    
    ```java
    import org.springframework.stereotype.Component;
    
    @Component
    public class MyComponent { // 클래스 이름의 첫글자를 소문자로 바꿔서 등록된다.
        public void doSomething() {
            System.out.println("Component Bean 실행!");
        }
    }
    ```
    
2. 빈 설정파일에 (Bean Configuration File)에 직접 빈 등록 (`@Configuration` + `@Bean` 방식)
    - 외부 라이브러리나 직접 컨트롤할 수 없는 클래스를 빈으로 등록할 때 유용하다.
    - 일반적으로 `xxxConfiguration`으로 명명한다.
    
    ```java
    import org.springframework.context.annotation.Bean;
    import org.springframework.context.annotation.Configuration;
    
    @Configuration
    public class AppConfig {
    
        @Bean
        public MyComponent myComponent() {
            return new MyComponent();
        }
    }
    ```
    
3. XML 설정 파일을 통한 빈 정의
    
    스프링 부트에서는 XML에 대한 관리를 직접하지는 않아서 잘 사용하지 않음.
    
    ```java
    <beans>
        <bean id="myComponent" class="com.example.MyComponent"/>
    </beans>
    ```
    

### 빈의 사용방법

`ApplicationContext` 와 같은 스프링 컨테이너 API 를 통해 필요한 빈을 획득 (`getBean()`) 하여 애플리케이션 코드에서 사용합니다. 주로 의존성 주입 (DI) 을 통해 빈을 프레임워크로부터 주입받아 사용하는 것이 일반적입니다.

이렇게 생성된 빈은 스프링 컨테이너에 의해 생명주기가 관리된다.

### 빈의 생명주기

총 단계: 생성 → 의존성 주입 (DI) → 초기화 → 사용 → 소멸

1. **Bean 생성(Instantiation)**
    - 스프링 컨테이너가 빈 정의를 확인하고, 빈 클래스로부터 인스턴스를 생성합니다.
2. **의존성 주입(Dependency Injection, DI)**
    - `@Autowired` 어노테이션, 생성자 주입, 세터 주입 등을 통해 필요한 다른 빈을 주입받습니다.
3. **초기화(Initialization) 단계**
    - 빈 생성과 의존성 주입이 끝난 후, 필요한 초기화 로직을 수행합니다.
    - 어노테이션 기반(`@PostConstruct`) 혹은 XML/Java Config 설정(`init-method`)을 통해 초기화 메서드를 지정할 수 있습니다.
        - `InitializingBean` 인터페이스로 초기화 단계 구현가능하다. 과거에 많이 사용됐었다.
    - 초기화 과정에서 추가적으로 `BeanPostProcessor`들이 개입하여 빈의 프로퍼티를 확인하거나, AOP 적용 등 다양한 후처리를 수행할 수 있습니다.
4. **사용(Use)**
    - 애플리케이션 로직에서 빈을 활용합니다.
    - 싱글톤 스코프 빈은 컨테이너가 종료되기 전까지 계속 유지되고, 프로토타입 스코프 빈은 획득 시마다 새 인스턴스로 사용됩니다.
5. **소멸(Destroy) 단계**
    - 스프링 컨테이너가 종료되거나, 빈이 더 이상 필요 없을 때 소멸 과정을 거칩니다(주로 싱글톤이나 기타 웹 스코프에서 해당).
    - `@PreDestroy` 어노테이션, XML/Java Config 설정(`destroy-method`)을 통해 소멸 직전에 필요한 정리 작업(리소스 해제 등)을 수행할 수 있습니다.
        - `DisposableBean` 인터페이스도 있다. (`@PreDestroy` 를 훨씬 많이 사용)
    - 프로토타입 스코프 빈의 경우 컨테이너가 소멸 과정을 관리하지 않으므로, 사용자가 직접 소멸 처리를 해주어야 할 수 있습니다.

<aside>
💡

빈의 스코프

빈은 생성과 관리의 범위를 지정할 수 있는 스코프를 가진다.

1. **Singleton (기본 스코프)**
    
    일단, 빈은 싱글톤으로 구성된다!
    
    - *싱글톤처럼 관리한다는 것으로 싱글톤 패턴과는 별개*
    - 애플리케이션 전체에서 단 하나의 객체 인스턴스만을 유지합니다.
    - 스프링 컨테이너가 구동될 때 빈을 한 번만 생성하고, 이후에는 동일한 객체를 반환합니다.
    - **가장 일반적인 스코프**이며, 스프링 Bean의 기본 스코프입니다.
2. **Prototype**
    - 빈을 요청할 때마다 새로운 객체 인스턴스를 생성합니다.
    - 상태를 가지는 객체를 매번 새롭게 필요로 하는 경우에 사용됩니다.
    - 생성 시점마다 새 객체가 생성되므로, 소멸 시점 관리는 컨테이너가 아닌 사용자가 직접 담당해야 하는 경우가 많습니다. (여전히 GC 대상이다)
3. **Request**
    - 웹 애플리케이션 환경에서, **HTTP 요청 당 하나의 빈 인스턴스**가 생성되고 요청이 끝나면 소멸됩니다.
    - 주로 Spring MVC의 요청 처리 과정에서 사용됩니다.
    - WebApplicationContext에서만 동작. ApplicationContext에서 동작 X
    - 프록시 사용이 필요하다.
        
        ```java
        @Scope(value = "request", proxyMode = ScropedProxyMode.INTERFACES)
        ```
        
4. **Session**
    - 웹 애플리케이션 환경에서, **HTTP 세션 당 하나의 빈 인스턴스**를 유지합니다.
    - 사용자별 세션 범위로 객체를 관리해야 할 때 사용됩니다.
5. **GlobalSession**
    - 포털(Portal)처럼 전역 세션 범위를 가지는 환경에서 사용되는 스코프입니다. (일반적인 Web 애플리케이션에서는 자주 사용되지 않습니다.)
</aside>

그렇다면 의존성 주입 (DI)이란 도데체 무엇일까?

# 의존성 주입 (DI, Dependency Injection)

객체가 필요로 하는 의존 객체를 **직접 생성**하지 않고, **외부**에서 **주입**받는 **원리** 혹은 **기법**

<aside>
💡

IoC (제어의 역전)와 DI (의존성 주입)의 관계

스프링 프레임워크는 IoC 컨테이너를 제공하며, **DI** 방식을 통해 객체 간의 의존성을 설정하여 IoC를 달성합니다.

</aside>

의존성 주입의 장점

1. 객체 간 결합도 감소 (Decoupling)
    
    객체가 어떤 구현체를 사용하는지 외부에서 결정하므로, Mock 객체 등으로 쉽게 교체할 수 있어 테스트가 편리하고 재사용성이 높아집니다.
    
2. 인터페이스 기반 설계 장려
3. 테스트 및 재사용성 향상
    
    객체가 어떤 구현체를 사용하는지 외부에서 결정하므로, Mock 객체 등으로 쉽게 교체할 수 있어 테스트가 편리하고 재사용성이 높아집니다.
    
4. 개발 생산성 및 유지보수성 향상

### DI 구현 방식

1. 생성자 주입 (Constructor Injection)
    
    생성자를 통해 의존성을 주입하는 방법 (가장 권장하는 방법)
    
    - 필수 의존성을 객체 생성 시점에 모두 주입받아, 객체가 불완전한 상태가 되지 않도록 보장한다.
    - 테스트 및 유지보수에 유리하고, **불변성**(immutable)을 지키기에도 수월하다.
    
    ```java
    @Service
    //@Autowired, 최신 버전의 스프링에서는 생략 가능, 의존성 주입
    public class MyService {
        private final MyRepository myRepository;
        
        public MyService(MyRepository myRepository) { // ✅ 직접 new MyService 객체를 생성하지 않아도 자동으로 가져온다.
            this.myRepository = myRepository;
        }
    }
    ```
    
    - Lombok - `@RequiredArgsConstructor` 으로 편리하게 생성자 주입 가능하다.
    
    ```java
    @RequiredArgsConstructor
    public class CopurchasingService {
    
        private final CopurchasingRepository copurchasingRepository;
        private final UserRepository userRepository;
         
        ...
    }
    ```
    
2. Setter 주입 (Setter Injection)
    
    세터 메서드를 통해 의존성을 주입하는 방법
    
    - 선택적 의존 관계가 필요한 경우 사용
    - 필요하지 않은 상황에서 남발하면 객체의 상태가 변경되어 예측하기 어려울 수 있다.
    
    ```java
    @Service
    public class MyService {
        private final MyRepository myRepository;
        
        @Autowired
        public MyService(MyRepository myRepository) {
            this.myRepository = myRepository;
        }
    }
    ```
    
3. 필드 주입 (Field Injection)
    
    클래스의 멤버 변수에 직접 주입하는 방법
    
    - `@Autowired`를 붙여 의존 객체를 주입받는 방식
    - 테스트나 리팩토링 시 불편함이 많고, 순환 참조 문제가 발생하기 쉬워 **권장되지 않는다.**
    
    ```java
    @Service
    public class MyService {
        @Autowired
        private MyRepository myRepository;
    }
    ```
    

이때, `final` 필드와 함께 생성자 주입을 사용하면, 의존 객체가 변경되지 않는 안전한 구조를 만들 수 있다.

### DI의 사용 이유를 예제를 통해 알아보자

DI 사용 전

```java
// 1) UserRepository 인터페이스
public interface UserRepository {
    User findUserById(int userId);
}

// 2) DatabaseUserRepository (UserRepository 구현체)
public class DatabaseUserRepository implements UserRepository {
    @Override
    public User findUserById(int userId) {
        // 실제 DB 연결 로직이 있다고 가정
        System.out.println("DatabaseUserRepository: 데이터베이스에서 사용자 정보 조회");
        return new User(userId, "User" + userId);
    }
}

// 3) UserService (UserRepository 의존 - 하지만 DI 미적용)
public class UserService {
    private DatabaseUserRepository userRepository; // 구체 클래스에 직접 의존

    public UserService() {
        // ✅ UserService 내부에서 DatabaseUserRepository를 직접 생성
        // -> 높은 결합도 (DI 미적용)
        this.userRepository = new DatabaseUserRepository();
    }

    public User getUser(int userId) {
        return userRepository.findUserById(userId);
    }
}

// 4) Main
public class Main {
    public static void main(String[] args) {
        // UserService 객체를 생성하면, 내부적으로 DatabaseUserRepository도 함께 생성됨
        UserService userService = new UserService();

        // userService가 구체 클래스(DatabaseUserRepository)에 직접 의존하므로
        // 다른 구현체로 교체하기가 어렵고, 테스트 시 Mock으로 대체하기도 번거롭다.
        
        User user = userService.getUser(1);
        System.out.println("User: " + user.getUserId() + ", " + user.getName());
    }
}

```

DI 사용 후

```java
// 1) UserRepository 인터페이스 (동일)
public interface UserRepository {
    User findUserById(int userId);
}

// 2) DatabaseUserRepository (UserRepository 구현체) - 실제 DB 연동용 (동일)
public class DatabaseUserRepository implements UserRepository {
    @Override
    public User findUserById(int userId) {
        System.out.println("DatabaseUserRepository: DB 조회");
        return new User(userId, "User" + userId);
    }
}

// 2-1) 추가 구현체: MockUserRepository (UserRepository 구현체) - 테스트용
public class MockUserRepository implements UserRepository {
    @Override
    public User findUserById(int userId) {
        System.out.println("MockUserRepository: 가짜 사용자 정보 반환");
        return new User(userId, "MockUser" + userId);
    }
}

// 3) UserService (UserRepository 의존 - DI 적용)
// ✅ 다형성에 초점을 맞춘 설계?
public class UserService {
    private final UserRepository userRepository; // 인터페이스 타입에 의존

    // 생성자 주입(권장)
    // -> UserService에서는 어떤 구현체가 들어오는지 몰라도 동작 가능
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public User getUser(int userId) {
        return userRepository.findUserById(userId);
    }
}

// 4) Main
public class Main {
    public static void main(String[] args) {
        // 실제 운영 환경(Production): DatabaseUserRepository를 사용
        UserRepository realRepo = new DatabaseUserRepository();
        UserService userServiceProd = new UserService(realRepo);
        User userProd = userServiceProd.getUser(1);
        System.out.println("Prod: " + userProd.getUserId() + ", " + userProd.getName());

        // 테스트 환경(Test): MockUserRepository로 쉽게 교체 가능
        UserRepository mockRepo = new MockUserRepository();
        UserService userServiceTest = new UserService(mockRepo);
        User userTest = userServiceTest.getUser(2);
        System.out.println("Test: " + userTest.getUserId() + ", " + userTest.getName());
    }
}

```

<aside>
💡

DIP (SOLID 원칙의 D)

객체 지향 설계에서 “상위 모듈이 하위 모듈에 의존하면 안 된다”는 개념
즉, “구체적인 구현이 아닌, 추상화된 인터페이스에 의존하라”는 원칙

→ 하위 모듈의 구체적인 내용에 클라이언트가 의존하게 되어 하위 모듈에 변화가 있을 때마다클라이언트나 상위 모듈의 코드를 자주 수정해야 되기 때문에

```java
// 변수 타입을 고수준의 모듈인 인터페이스 타입으로 선언하여 저수준의 모듈을 할당
List<String> myList = new ArrayList()<>;
    
Set<String> mySet = new HashSet()<>;

Map<int, String> myMap = new HashMap()<>;
```

</aside>
