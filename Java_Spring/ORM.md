# ORM (Object-Relational Model)

**객체지향 프로그래밍 언어**에서 사용하는 **객체**를, **관계형 데이터베이스**(예: MySQL, PostgreSQL 등)의 **테이블**과 자동으로 매핑하여 다룰 수 있게 해주는 기술

개발자가 **객체지향적인 방식**으로 데이터베이스 작업을 수행하도록 돕는 역할을 한다.

<br/>

**그렇다면 ORM이 등장하기 이전에 무슨 문제점들이 있었을까?**

<br/>

## 등장 이유

**패러다임 불일치 문제**

- **객체지향 프로그래밍(OOP)**
    - 데이터를 **객체**(클래스) 단위로 구성하고, **상속**, **연관관계**, **다형성** 등을 사용
    - 객체 간의 **그래프 탐색**으로 데이터에 접근
- **관계형 데이터베이스(RDBMS)**
    - 데이터를 테이블과 컬럼, 행(Row)으로 표현
    - SQL 쿼리를 통해 데이터 조회/수정/삭제

이 둘은 데이터 구조와 접근 방식이 달라서, 애플리케이션에서 객체-테이블 간 **수작업** 변환을 해야 하는 **패러다임 불일치**가 발생합니다.

ORM은 이러한 변환을 **자동화**해, 개발자가 객체 중심의 코드만 작성해도 DB 연동이 가능하도록 해줍니다.

사실, ORM(JPA) 이전에 **SQL Mapper**를 사용했었다. 매핑은 자동으로 해주지만 여전히 SQL 로직을 개발자가 주도적으로 작성해야 해서 불편함이 존재했었다.

**SQL Mapper (예: MyBatis)**

- SQL 쿼리를 XML 또는 애노테이션으로 직접 작성하지만, 결과 매핑은 자동으로 해주는 방식
- 개발자가 **SQL 주도**로 로직을 작성하되, 매핑은 프레임워크가 도와주는 형태
- 학습 곡선이 낮다.

<br/>

**ORM을 사용하면 간단하게 DB에 접근하여 로직을 수행할 수 있다.**

<br/>

## 사용 방법 (JPA 예시)

1. **프로젝트 설정**
    - Maven/Gradle 의존성에 `spring-boot-starter-data-jpa`, DB 드라이버, `hibernate` 추가
        
        ```xml
        <!-- Spring Boot JPA + Hibernate -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        
        <!-- H2 (In-Memory DB) -->
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <scope>runtime</scope>
        </dependency>
        ```
        
    - `application.properties`(또는 `application.yml`)에서 DB 연결정보(`spring.datasource.url` 등), JPA 설정(`spring.jpa.hibernate.ddl-auto` 등) 지정
        
        ```xml
        spring.datasource.url=jdbc:h2:mem:testdb
        spring.datasource.driver-class-name=org.h2.Driver
        spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
        spring.jpa.hibernate.ddl-auto=update
        ```
        
2. **엔티티(Entity) 클래스 정의**
    - `@Entity`, `@Table`, `@Id` 등 JPA 애노테이션을 사용해 매핑 정보를 설정
    - ex) `User.java` (id, name, email 필드 등)
3. **매핑 정보 설정**
    - 필요한 경우 `@Column`, `@ManyToOne`, `@OneToMany`, `@Inheritance` 등을 사용해 컬럼, 연관관계, 상속 매핑 설정
    
    ```xml
    import jakarta.persistence.*;
    
    @Entity
    @Table(name = "users") // DB 테이블 매핑
    public class User {
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY) // Auto Increment 설정
        private Long id;
    
        private String name;
        private String email;
    
        // 기본 생성자 (JPA 필수)
        public User() {}
    
        // 생성자
        public User(String name, String email) {
            this.name = name;
            this.email = email;
        }
    
        // Getter & Setter
        public Long getId() { return id; }
        public String getName() { return name; }
        public String getEmail() { return email; }
    }
    ```
    
4. **데이터 접근 코드**
    - Spring Data JPA의 `JpaRepository` 인터페이스를 상속하거나, `EntityManager`를 직접 주입받아 DB 작업 수행
        
        
        ```java
        import org.springframework.data.jpa.repository.JpaRepository;
        import org.springframework.stereotype.Repository;
        
        @Repository
        public interface UserRepository extends JpaRepository<User, Long> {
            User findByName(String name); // SQL 없이 자동으로 구현됨!
        }
        ```
        
        <img width="428" alt="image" src="https://github.com/user-attachments/assets/2fcf9f75-fb40-414d-9830-9833b1125a1a" />

        
5. **실행 및 연동**
    - 스프링 부트가 기동되면서 JPA/Hibernate 초기화, `UserRepository` 등을 빈으로 등록
    - 엔티티 객체를 저장/조회 시 ORM이 자동으로 SQL을 생성・실행
    - 실제 예시
        
        ```java
        // 예시: 엔티티
        @Entity
        @Table(name = "users")
        public class User {
            @Id
            private Long id;
            private String name;
            private String email;
            // getter, setter, default constructor...
        }
        
        ```
        
        ```java
        // 예시: 스프링 데이터 JPA Repository
        public interface UserRepository extends JpaRepository<User, Long> {
            User findByName(String name); // findBy는 예약어, Name은 속성
            User findByEmail(String email); // findBy는 예약어, Name은 속성
        }
        ```
        
        ```java
        // 예시: 서비스 계층
        @Service
        public class UserService {
            @Autowired
            private UserRepository userRepository;
        
            public void saveUser(User user) {
                userRepository.save(user); // INSERT/UPDATE SQL 자동 생성
            }
        
            public User getUserByName(String name) {
                return userRepository.findByName(name); // SELECT SQL 자동 생성
            }
        }
        
        ```
        
<br/>

**이런 ORM은 SQL 작성 없이 간편하게 데이터베이스에 접근할 수 있다. 이외에도 다양한 장점들이 있다.**

<br/>

## 장점

1. **생산성**: 반복적 DB 코드(쿼리, 매핑 등)를 자동화, 개발 속도 증가
2. **유지보수성**: 엔티티와 매핑 정보만 수정하면 되므로, DB 스키마 변경에 유연
3. **객체지향적**: 연관관계, 상속, 캡슐화 등 OOP 개념을 DB 접근에도 적용 가능
4. **보안/안정성**: 자동 파라미터 바인딩으로 **SQL Injection** 위험이 줄어듦
5. **DB 이식성**: 특정 벤더 종속성이 낮고, 설정만 바꾸면 타 DB로의 전환 가능

<br/>

**하지만, 기술의 Trade-Off로 인해 당연히 단점도 존재한다.**

<br/>

## 단점

1. **학습 곡선**: ORM 내부 동작(JPA 영속성 컨텍스트, 캐싱, 연관관계) 이해가 필요
2. **성능 이슈**: 무작정 사용 시 **N+1 문제**, ~~**지연 로딩**~~ 이슈 등 발생 가능
    
    <aside>
    📌
    
    **N+1 문제**
    
    1번의 쿼리로 여러 개의 엔티티를 조회했는데, **연관된 엔티티를 가져오기 위해 추가로 N개의 쿼리가 발생하는 문제.**
    
    예시
    
    ```java
    List<Team> teams = teamRepository.findAll(); // 팀 리스트 조회
    for (Team team : teams) {
        System.out.println(team.getUsers().size()); // 각 팀에 속한 사용자 수 조회
    }
    ```
    
    ```java
    SELECT * FROM team; -- (1개의 메인 쿼리)
    SELECT * FROM users WHERE team_id = ?; -- (N개의 추가 쿼리 발생)
    SELECT * FROM users WHERE team_id = ?;
    ...
    ```
    
    해당 문제는 Fetch 전략, JPQL(Java Persistence Query Language) Fetch 조인 등을 통해 최적화해야 한다.
    
    ```java
    @Query("SELECT t FROM Team t JOIN FETCH t.users")
    List<Team> findAllWithUsers();
    ```
    
    </aside>
    
3. **완벽 추상화의 어려움**: 복잡한 SQL, DB 특화 기능(Stored Procedure, Window 함수 등)은 직접 SQL 작성 필요
4. **ORM 의존성**: 프로젝트가 ORM 프레임워크에 깊이 의존, 특정 상황에서 제약이 있을 수 있음
