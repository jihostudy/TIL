> 다른 언어와 비슷한 점이 많아, 자바만의 특별한 내용만 정리

[중첩된 반복문 빠져나오는 방법]

Outer 구문에 레이블을 만들어 두면, `break 레이블`을 통해 중첩 반복문을 빠져나올 수 있다.

- `Flag`를 따로 생성하지 않아도 된다.

```java
Outer:
for(int i = 0; i < 10; i++){
	for(int j = 0; j < 10; j++) {
		System.out.println("i: " + i + " j: " + j);
		if(i == 1) {
			break Outer; // ✅ 레이블을 추가하여 한번에 빠져나올수 있다.
		}
	}
}
```
