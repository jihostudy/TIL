# AOP (Aspect Oriented Programming, 관점 지향 프로그래밍)

핵심 관심사(Core Concerns)와 횡단 관심사(Cross-Cutting Concerns)를 분리하여 **모듈화**하는 프로그래밍 패러다임
 
<aside>
📌

핵심 관심사 및 횡단 관심사란?

핵심 관심사: 애플리케이션의 비즈니스 로직 그 자체 (평소에 구현하던 내용이라고 생각)

횡단 관심사: 여러 핵심 로직(클래스, 메서드 등)에 **공통 적용**되는 기능 (ex. 로깅, 보안, 트랜잭션, 성능 모니터링 등) 혹은 핵심 로직과는 부가적인 기능

</aside>

<br/>

**그렇다면 왜 핵심 관심사와 횡단 관심사를 “분리” 하는지 알아보자.**

<br/>

## AOP의 동기

AOP를 사용하는 이유를 알기 위해서는 사용하기 이전의 고충에 대해 이해해보면 된다.

**📌 시나리오 요구사항**

1. `OrderService` 클래스의 주문 관련 메서드 실행 전/후에 로깅(Log)을 추가하고 싶다.
2. 주문 생성(`createOrder()`)의 **실행 시간을 측정**하고 싶다.

### 1. AOP가 적용되지 않았을 때

AOP 없이 `OrderService`에서 **직접 로깅과 실행 시간을 측정**하는 경우, **코드가 지저분해지고 유지보수가 어려워진다.**

```java
import org.springframework.stereotype.Service;

@Service
public class OrderService {
    public void createOrder(String orderId) {
		    // 1️⃣ 실행 시간 측정 시작
        long startTime = System.currentTimeMillis(); 

        System.out.println("[LOG] createOrder 실행 시작: " + orderId);

        // 🛒 주문 생성 로직
        System.out.println("✅ 주문이 생성되었습니다. 주문 ID: " + orderId);

        System.out.println("[LOG] createOrder 실행 종료: " + orderId);

        long endTime = System.currentTimeMillis();
        System.out.println("⏳ 실행 시간: " + (endTime - startTime) + "ms");
    }

    public void cancelOrder(String orderId) {
        System.out.println("[LOG] cancelOrder 실행 시작: " + orderId);

        // 🛑 주문 취소 로직
        System.out.println("❌ 주문이 취소되었습니다. 주문 ID: " + orderId);

        System.out.println("[LOG] cancelOrder 실행 종료: " + orderId);
    }
}
```

### 2. AOP를 적용하여 비즈니스 로직에서 시간 측정 기능을 분리

1. **실행 시간을 측정 및 로깅하는 로직을 별개의 클래스로 분리**
    - `@Aspect`
        
        AOP 클래스로 정의
        
    - `@Pointcut("execution(* com.example.service.OrderService.*(..))")`
        
        적용할 클래스를 지정하는 방법
        
        - 예시에서는  `.OrderService.*(..)`  를 사용하여 OrderService의 모든 메소드에 적용함
    - `@Before`
        
        메서드 실행 전에 수행할 로직
        
    - `@After`
        
        메서드 실행 후 수행할 로직
        
    - `@Around`
        
        메소드 실행 전후에 수행하는 로직 (트랙잭션 처리 / 성능 측정에 자주 사용된다)
        

```java
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.*;
import org.springframework.stereotype.Component;

@Aspect  // AOP 클래스 정의
@Component  // 스프링 빈 등록
public class LoggingAspect {

    // 1️⃣ OrderService 클래스의 모든 메서드에 AOP 적용
    @Pointcut("execution(* com.example.service.OrderService.*(..))")
    public void orderServiceMethods() {}

    // 2️⃣ Before Advice: 메서드 실행 전 로그 출력
    @Before("orderServiceMethods()")
    public void logBefore() {
        System.out.println("[LOG] 메서드 실행 시작...");
    }

    // 3️⃣ After Advice: 메서드 실행 후 로그 출력
    @After("orderServiceMethods()")
    public void logAfter() {
        System.out.println("[LOG] 메서드 실행 종료...");
    }

    // 4️⃣ Around Advice: 실행 시간 측정
    @Around("orderServiceMethods()")
    public Object measureExecutionTime(ProceedingJoinPoint joinPoint) throws Throwable {
        long start = System.currentTimeMillis();

        Object result = joinPoint.proceed(); // 실제 메서드 실행

        long end = System.currentTimeMillis();
        System.out.println("⏳ 실행 시간: " + (end - start) + "ms");

        return result;
    }
}
```

1. **핵심 로직에서 AOP 관련 로직 제거**

🚀 **핵심 로직을 수정하지 않고도 로깅과 실행 시간을 측정할 수 있음! (매우 깔끔해진 코드)**

```java
import org.springframework.stereotype.Service;

@Service
public class OrderService {
    public void createOrder(String orderId) {
        // 🛒 주문 생성 로직
        System.out.println("✅ 주문이 생성되었습니다. 주문 ID: " + orderId);
    }

    public void cancelOrder(String orderId) {
        // 🛑 주문 취소 로직
        System.out.println("❌ 주문이 취소되었습니다. 주문 ID: " + orderId);
    }
}
```
<br/>

**이렇게 AOP로 구현하면 핵심 관심사에서 횡단 관심사를 분리할 수 있어 굉장히 간단한 코드 작성이 가능하다.**

<br/>
## AOP 사용 이유

1. 횡단 관심사 코드 중복 제거
2. 핵심 로직 코드 가독성 및 유지보수성 향상
3. 모듈성 · 재사용성 증가
    - 횡단 관심사를 `Aspect`라는 독립 모듈로 관리하므로, 다른 프로젝트나 모듈에 재사용 용이
    - 한 번 정의한 `Aspect`를 여러 곳에서 활용 가능
4. 비침투적 (Non-Invasive) 적용
    - 핵심 로직 코드를 직접 수정하지 않고도, ✅ Aspect를 **프록시** 방식으로 적용
        - Weaving 방식이 프록시 방식으로 Aspect를 먼저 실행 → 핵심 로직 코드 실행 순으로 적용됨.
            
            이러한 방식이 프록시 방식으로 적용된다고 하는것임.
            
    - 기존 코드 변경 없이 횡단 관심사 추가 / 제거 (유지보수) 가능하며 간편함

<br/>

**그렇다면, 스프링 AOP를 구성하는 요소와 구현하는 방법에 대해 알아보자.**

<br/>

## 스프링 AOP의 주요 개념

1. **Aspect**
    
    횡단 관심사 코드를 담는 **클래스** 단위 (클래스에 직접 적용)
    
    - `@Aspect` 어노테이션을 사용하여 정의
2. **Pointcut**
    - Advice가 적용될 **Join Point**(메서드 실행 지점 등)를 지정하는 표현식
    - 예) `@Pointcut("execution(* com.example.service.*Service.*(..))")`
        - `com.example.service` 패키지 내 `Service`로 끝나는 클래스의 모든 메서드를 매칭
3. **Advice (실제 활동)**
    - Aspect가 실제 수행하는 **횡단 관심사 기능**(로깅, 보안, 트랜잭션 등)
    - 실행 시점에 따라 여러 종류가 있음
        - **Before Advice**: 메서드 실행 전에 로직 수행 `@Before`
        - **After Returning Advice**: 메서드가 정상 종료된 후 로직 수행 `@AfterReturning`
        - **After Throwing Advice**: 메서드에서 예외 발생 시 로직 수행 `@AfterThrowing`
            
            ```java
            @AfterThrowing(pointcut = "execution(* com.example.service.*.*(..))", throwing = "ex")
            public void logException(Exception ex) {
                System.out.println("🚨 예외 발생: " + ex.getMessage());
            }
            ```
            
        - **After (Finally) Advice**: 메서드 실행 결과와 상관없이 항상 실행 `@After`
        - **Around Advice**: 메서드 실행 전후에 로직 수행 (가장 강력, 트랜잭션 처리/성능 측정에 자주 사용) `@Around`
4. **Join Point**
    - Advice가 **삽입**될 수 있는 **실제 실행 지점** (스프링 AOP는 주로 메서드 실행이 Join Point)
5. Weaving
    - Aspect(횡단 관심사)를 핵심 로직 코드에 **결합**하는 과정
        - 즉, **`Advice`(부가 기능)와 `Pointcut`(적용 위치)을 조합하여 실제 코드에 적용하는 단계!!**
    - Spring AOP는 주로 **런타임 프록시**(JDK 동적 프록시 or CGLIB)를 생성하여 Weaving을 수행
        - **즉, 실행 중에 동적 프록시를 생성하여 AOP를 적용하는 방식**
            - JDK 동적 프록시: 자바가 기본적으로 제공 / 인터페이스 기반으로 프록시를 동적으로 생성
            - CGLIB: 바이트코드를 조작해서 동적으로 클래스를 생성하는 기술
    
    <aside>
    📌
    
    **Weaving은 AOP가 설정되어 있으면 스프링이 자동으로 처리**해 주는 기능이다.
    
    즉, 개발자는 **별도로 Weaving을 직접 명시하거나 설정할 필요가 없다.** 
    
    </aside>
    
<br/>

**이렇게 주요 개념들을 실제로 적용하는 방법에 대해 알아보자.**

<br/>

## AOP 활성화 방법

1. **`@EnableAspectJAutoProxy`**
    - 스프링 부트에서도 AOP를 사용하려면 Java Config나 `@SpringBootApplication` 클래스에 `@EnableAspectJAutoProxy`를 붙여 **AspectJ 자동 프록시**를 활성화
    - 예)
        
        ```java
        @SpringBootApplication
        @EnableAspectJAutoProxy
        public class MySpringBootApplication {
            public static void main(String[] args) {
                SpringApplication.run(MySpringBootApplication.class, args);
            }
        }
        ```
        
2. **Aspect 클래스 등록**
    - `@Aspect` + `@Component`를 사용해 **스프링 빈**으로 등록
    - 스프링 부트는 컴포넌트 스캔을 통해 자동 인식

<br/>

**이렇게 좋은 AOP는 계속 사용하면 될까? 당연히 아니다.** 
**기술을 Trade-Off 관계에 있다. AOP의 단점을 알고 이를 토대로 주의해서 사용해야 한다.**

<br/>

## AOP의 단점 및 주의사항

1. (단점) 코드 흐름이 복잡해져 디버깅 및 유지보수가 어려워진다.
    
    지나치게 많은 AOP를 생성하면 코드 흐름 파악이 어려워질 수 있다.
    
2. (단점) 프록시 방식으로 인한 성능 오버헤드
    - 런타임 프록시 생성으로 인한 오버헤드가 있으나, 대체로 **비즈니스 로직 이점**이 더 큼
    - 성능이 매우 민감한 경우 테스트・검증이 필요
3. **(주의사항)** 스프링 AOP 제한
    - 기본적으로 **Spring Bean**(싱글턴) 메서드에만 적용
        
        **스프링 AOP는 Spring 컨테이너에서 관리하는 빈(Bean)에만 적용됨.**
        
    - `final`, `private` 메서드에는 적용되지 않음
        
        **JDK Dynamic Proxy 패턴을 사용하여** final 메서드에 적용 불가능.
        
        ```java
        @Service
        public class MyService {
            private void doSomething() { // ⚠️ AOP 적용 안 됨!
                System.out.println("실행 중...");
            }
        }
        ```
        
        ```java
        @Service
        public class MyService {
            public void doSomething() { // ✅ AOP 적용 가능!
                System.out.println("실행 중...");
            }
        }
        ```
        
    - 심화 사용 시 AspectJ 컴파일-타임 위빙 등도 고려 가능

<br/>

**AOP 관련 공부할때 자주 나오는 질문이 OOP와의 관계이다.**

<br/>

## AOP vs. OOP (보완 관계)

| 구분 | OOP (객체지향 프로그래밍) | AOP (관점 지향 프로그래밍) |
| --- | --- | --- |
| 주요 관심사 | **핵심 관심사**(비즈니스 로직)  클래스・객체 모델링 | **횡단 관심사**(로깅, 보안, 트랜잭션 등) Aspect로 분리 |
| 모듈화 단위 | 클래스(객체), 상속, 다형성, 캡슐화 등 | Aspect, Advice, Pointcut |
| 목적 | 비즈니스 로직 모델링, 재사용성・유지보수성 강화 | 횡단 관심사 모듈화, 코드 중복 제거,핵심 로직 가독성 향상 |
| 적용 대상 | 주로 엔티티・서비스・컨트롤러 등의 비즈니스 로직 | 로깅, 보안, 트랜잭션, 모니터링 등 공통 기능 |
| 관계 | 애플리케이션의 **핵심 설계 패러다임** | OOP로 풀기 어려운 **횡단 관심사 문제**를보완하는 **보조 패러다임** |

**핵심 요약**

- **OOP**: 핵심 비즈니스 로직 설계・구현에 적합
- **AOP**: 횡단 관심사를 모듈화하여 OOP로 모듈화하기 어려운 부분을 해결
- **서로 대체 관계가 아니라 보완 관계**이므로, AOP는 OOP 애플리케이션에 적용되어 전체 코드 품질을 높이는 역할을 합니다.
