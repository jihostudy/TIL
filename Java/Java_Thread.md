<a href="https://vivid-chamomile-2f5.notion.site/Lecture6-2-190d85adc2df806b9cc7f611201e747e?pvs=4">노션 노트 보기</a>

## 자바에서 스레드 생성 방법

- `Runnable` 인터페이스 활용
- `Thread` 클래스 활용

### 1. Runnable 인터페이스 활용

```java
class MyRunnable implements Runnable {
    public void run() {
        System.out.println("Runnable is running.");
        // 실행할 코드 작성
    }
}

MyRunnable myRunnable = new MyRunnable(); // Runnable 인터페이스를 갖는 객체 생성
Thread thread = new Thread(myRunnable);
thread.start();
```

Runnable은 인터페이스이기 때문에, 그 자체로 객체로 구현할 수 없습니다. 그래서 구현체를 직접 만들어 사용해야 한다. 

Runnable 인터페이스에 선언되어 있는 것은 `run()` 메서드 하나 뿐이다.  → Runnable을 `implement`한 모든 클래스는 `run()` 함수를 포함해야 합니다.

해당 `run()` 메서드는 쓰레드가 시작 되었을 때 수행되는 기능을 작성할 수 있습니다.

### 2. Thread 클래스 활용

```java
class MyThread extends Thread {
    public void run() {
        System.out.println("Thread is running.");
        // 스레드가 실행할 코드를 여기에 작성
    }
}
```

Thread 클래스는 Runnable 인터페이스를 구현해 놓은 클래스이다. 

그렇기 때문에 Runnable 인터페이스에서 강제되는 `run()` 메서드 또한 작성해 주어야 합니다.

<aside>
💡

Runnable 인터페이스 / Thread 클래스 어떤 것을 현업에서 더 자주 사용할까요?

사실은 두가지 전부 사용하지 않습니다.

자바로 직접 스레드를 만들기보다 타 라이브러리를 사용한다.

- Thread 클래스를 상속하는 방법은 다중 상속이 불가능해서 선호되는 방법은 아니다. 둘중에 골라야 한다면 인터페이스를 사용해서 확장성을 열어두는 편이 좋다.
    - Runnable 방식은 직접 실행이 불가능하고 Thread 에게 위임해서 실행을 해야 하지만 Thread 클래스를 활용한 방식은 직접 실행할 수 있.
</aside>

### 실제 코드를 통한 실행 방법

```java
public class Main {
	public static void Main(String[] args){
		// 1️⃣ Runnable 활용
		MyRunnable myRunnable = new MyRunnable(); // Runnable 객체 생성
    Thread thread = new Thread(myRunnable); // Thread 객체 생성
		thread.start(); // 스레드 시작
		
		
		// 2️⃣ Thread 활용
		MyThread t = new MyThread(); // 스레드 객체 생성
		t.start(); // 스레드 시작
		
		System.out.println("main is end");
	}
}
// 결과 (항상 동일하지 않음. 스레드의 실행 순서는 보장할 수 없음)
Runnable is running.
Thread is running.
main is end
```

<img width="427" alt="image" src="https://github.com/user-attachments/assets/029cf1db-1e82-4edf-a958-8d41bb0314d7" />


쓰레드가 종료되는 시점은 바로 `run()` 메서드에 작성한 코드가 종료 되면 쓰레드가 종료되게 된다.

예시 코드에서는 print로 간단한 예시라 어느정도 종료 시점이 예측이 되지만, 실무에서는 예측 할 수 없는 경우가 매우 많다.

## 쓰레드를 통제방법

| 메서드명 | 설명 |
| --- | --- |
| `start()` | 새로운 스레드를 시작하고, run 메서드를 호출 |
| `run()` | 스레드가 실행할 코드를 포함, 직접 호출하는 것이 아니라 start() 에 의해 자동으로 호출 |
| `sleep(long ms)` | 스레드를 지정된 ms 동안 일시 중지 |
| `join()` | 스레드의 실행이 완료될 때까지 현재 스레드를 대기 |
| `interrupt()` | 수행중인 스레드에 종료 요청을 보냄  |

<aside>
💡

`run()` vs `start()` 헷갈리지 말기

`run()`은 스레드 내부에서 실행하는 코드며, 스레드 자체를 실행시키는 것은 `start()` 이다.

</aside>

- interrupt() 로 인해 발생하는 InterruptedException이란?

### `thread.sleep(long ms)` - 스레드 대기 하기

```java
public class Main {
    static int num = 1;

    public static void main(String[] args) {
        // Runnable 활용
        MyRunnable myRunnable = new MyRunnable(); // Runnable 객체 생성
        Thread thread = new Thread(myRunnable); // Thread 객체 생성
        thread.start(); // 스레드 시작

        // Thread 활용
        MyThread t = new MyThread(); // 스레드 객체 생성
        t.start(); // 스레드 시작

        System.out.println("main is end");
    }

    static class MyThread extends Thread {
        public void run() {
            try {
                Thread.sleep(1000);
                System.out.println("Thread is running.");
            } catch (InterruptedException ie) {
                ie.printStackTrace();
            }
        }
    }

    static class MyRunnable implements Runnable {
        public void run() {
            System.out.println("Runnable is running.");
        }
    }

}
// 결과
Runnable is running.
main is end
Thread is running. // Thread.sleep(1000) 으로 인해 마지막에 실행된다.
```

### `thread.join()` - 특정 스레드가 완료 될 때까지 대기하기

- 매개 변수로 long이 입력이 되었을 경우 밀리 초 단위로 대기 했다가 다음 작업을 수행한다.

```java
public class Main {
    static int num = 1;

    public static void main(String[] args) {
        // Runnable 활용
        MyRunnable myRunnable = new MyRunnable(); // Runnable 객체 생성
        Thread thread = new Thread(myRunnable); // Thread 객체 생성
        thread.start(); // 스레드 시작

        // Thread 활용
        MyThread t = new MyThread(); // 스레드 객체 생성
        t.start(); // 스레드 시작

        try {
            t.join(); // t가 종료될때까지 기다림
        } catch (InterruptedException ie) {
            ie.printStackTrace();
        }

        System.out.println("main is end");

    }

    static class MyThread extends Thread {
        public void run() {
            try {
                Thread.sleep(1000);
                System.out.println("Thread is running.");
            } catch (InterruptedException ie) {
                ie.printStackTrace();
            }
        }
    }

    static class MyRunnable implements Runnable {
        public void run() {
            System.out.println("Runnable is running.");
        }
    }

}
// 결과
Runnable is running.
Thread is running.
main is end // t.join()으로 인해 항상 마지막에 실행됨
```

### `thread.interrupt()` - 종료 요청 보내기

```java
public class Main {
    static int num = 1;

    public static void main(String[] args) {
        // Runnable 활용
        MyRunnable myRunnable = new MyRunnable(); // Runnable 객체 생성
        Thread thread = new Thread(myRunnable); // Thread 객체 생성
        thread.start(); // 스레드 시작

        // Thread 활용
        MyThread t = new MyThread(); // 스레드 객체 생성
        t.start(); // 스레드 시작

        try {
            t.interrupt();
            t.join();
        } catch (InterruptedException ie) {
            ie.printStackTrace();
        }

        System.out.println("main is end");

    }

    static class MyThread extends Thread {
        public void run() {
            try {
                Thread.sleep(1000);
                System.out.println("Thread is running.");
            } catch (InterruptedException ie) {
                ie.printStackTrace();
            }
        }
    }

    static class MyRunnable implements Runnable {
        public void run() {
            System.out.println("Runnable is running.");
        }
    }

}
```

Interrupt 는 해당 메서드로 종료 요청을 보내 InterruptedException을 발생 시키며 중단 시킵니다. 

## 정리 키워드

<aside>
💡

컨텍스트 스위칭

프로세스 스케쥴링 과정에서 프로세스를 변경하면서 생기는 시간

Context는 프로세스와 관련된 데이터의 집합이며, Interrupt (I/O, Clock Interrupt 등) 이후 Context Saving → Context Restoring → Context Switching 과정을 컨텍스트 스위칭 과정으로 칭한다.

</aside>

<aside>
💡

스레드 오버헤드

스레드 오버헤드는 스레드를 생성하고, 스케쥴링하고, 컨텍스트 스위칭하는 비용 등을 합친 것을 의미한다.

스레드를 무작정 많이 생성하는 것이 아닌, 필요한 스레드만 유동적으로 유지하는 것이 중요하다.

</aside>

<aside>
💡

임계 영역

(교안) Code Segment that Access shared Data

멀티 프로세스, 멀티 스레드 환경에서 동시에 접근할 수 있는 데이터 영역을 의미한다.

임계 영역은 데이터 무결성을 헤칠 수 있어서 동기화를 위한 기법을 통해 관리해야 한다.

</aside>

<aside>
💡

자바에서 Thread Class를 상속 받는 것과 Runnable Interface를 사용하는것의 차이

Thread Class는 객체 상속을 통해 수행하므로, 다중 상속을 지원하지 않는 자바에서는 확장 가능한 코드가 아니다.

다만, Runnable Interface로 스레드를 구현하면, 다중 인터페이스를 통해 확장 가능한 코드로 구현이 가능하다.

- Runnable 객체를 생성하는 점이 두 방법의 차이이기도 하다.
</aside>

<aside>
💡

`synchronized` 을 이용한 동시성 관리 방법

`synchronized` 키워드가 붙은 필드, 함수는 한 번에 하나의 스레드에서만 접근이 가능하다.

- Lock / UnLock 하여 동시성을 관리하는 방법
    - read & write의 원자성(atomic)을 보장하는 방법
- 메소드를 락하는 경우 `Critical Section`이 아닌 영역에 대한 Lock을 수행할 수 있어서 비효율적이다.

```java
class Counter {
    private int count = 0;

    public synchronized void increment() { // 동기화 메서드
        count++;
    }

    public synchronized int getCount() {
        return count;
    }
}
```

</aside>

<aside>
💡

`AtomicInteger`을 이용한 동시성 관리 방법

CAS기반의 동시성 제어 방법이다.

CAS(Compare And Swap)란 변수의 값을 변경하기 전에 기존에 가지고 있었던 값과 현재의 값이 같은 경우에만 새로운 값으로 할당하는 방법이다.

- Lock을 걸지 않아서 다른 스레드에서 접근 가능하다.
- CAS는 하드웨어의 도움을 받으며, `synchronized` 보다 좋은 성능을 지녔다.

```java
public class AtomicExample {
    int val;
    
    public boolean compareAndSwap(int oldVal, int newVal) {
        if(val == oldVal) {
            val = newVal;
            return true;
        } else {
            return false;
        }
    }
}
```

사용방법

- 각 AtomicType에 따른 메소드를 제공한다. [(javadoc에서 Atomic 메소드 찾기)](https://docs.oracle.com/javase/8/docs/api/index.html?java/util/concurrent/atomic/AtomicBoolean.html)

```java
import java.util.concurrent.atomic.AtomicInteger;

class AtomicCounter {
    private AtomicInteger count = new AtomicInteger(0);

    public void increment() {
        count.incrementAndGet(); // 동기화 없이 원자적 증가
    }

    public int getCount() {
        return count.get();
    }
}

```

</aside>

<aside>
💡

`volatile`을 이용한 동시성 제어 방법

`volatile`은 매개 변수의 값을 CPU Cache에 저장하여 사용하는 것이 아닌, Memory에 위치시켜 읽는 방법이다.

- 당연히 캐시가 접근 속도가 빠르기 때문에, 속도는 느리다

단, 멀티 스레드 환경에서 여러개의 스레드가 동시에 Write하는 상황에서는 동시성(Race Condition)을 해결할 수 없습니다.

- 따라서, `syncrhonized` 까지 활용하여 데이터의 원자성을 지켜야 한다.

```java
예시
Thread-1이 값을 읽어 1을 추가하는 연산을 진행한다.
추가하는 연산을 했지만 아직 Main Memory에 반영되기 전 상황이다.

Thread-2이 값을 읽어 1을 추가하는 연산을 진행한다.
추가하는 연산을 했지만 아직 Main Memory에 반영되기 전 상황이다.

두 개의 Thread가 1을 추가하는 연산을 하여 최종결과가 2가 되어야 하는 상황이지만?
각각 결과를 Main Memory에 반영하게 된다면 1만 남는 상황이 발생하게 된다.
```

</aside>

<aside>
💡

자바 언어에서 지원하는 동시성 관리(간단하게 정리)

- syncrhonized
- volatile
- AtomicIneger
- Thread Safe한 객체를 사용하기
    - `java.util.concurrent` 패키지에서 제공한다.
- ReentrantLock
    - 명시적으로 lock, unlock을 수행할 수 있도록 구현하는 방법 제공
    - Race condition / Deadlock 등 오류를 발생시킬 수 있는 여지가 많아 신중하게 사용해야 한다.
    
    ```java
    import java.util.concurrent.locks.Lock;
    import java.util.concurrent.locks.ReentrantLock;
    
    class Counter {
        private int count = 0;
        private final Lock lock = new ReentrantLock();
    
        public void increment() {
            lock.lock(); // 락 획득
            try {
                count++;
            } finally {
                lock.unlock(); // 반드시 해제해야 함
            }
        }
    
        public int getCount() {
            return count;
        }
    }
    ```
    
</aside>
