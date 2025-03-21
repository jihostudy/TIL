### 재조정 과정

React가 DOM 트리를 재구성하는 방법

리액트에서는 Reconcilitation (재조정) 과정을 통해, Actual DOM 과 Virtual DOM의 Diff(차이점)만을 알아내서 새로운 Browser DOM을 렌더링한다.

이는, 모든 노드를 렌더링하지 않고 바뀐 State 노드만 변경하여 렌더링 최적화를 이룬 것이라고 볼 수 있다.

<img width="431" alt="image" src="https://github.com/user-attachments/assets/1249abac-0013-444a-a822-bc72d56c6afa" />

<br />

이는 총 2가지 단계로 이루어진다.

1. **Reconciler**
    - Current 트리와 작업 중(Work in Progress) 트리의 **차이점을 발견하는 역할**을 한다.
    - React 내부의 **Diffing Algorithm**을 사용하여 바뀐 점을 알아낸다
    
    > 리액트에서는 O(N3)의 비효율적인 diffing-algorithm을 개선하였다.
    AI에서 자주 사용하는 Heuristic O(n) 알고리즘을 사용하였다.
    > 


2. **Renderer**
    - Reconciler로부터 전달받은 Diff를 토대로, **Current 트리를 바꾸는 역할을 수행**한다.
    

위에서, 리액트의 Reconciler **diffing-algorithm**이 **Heruistic 알고리즘**을 사용하여 DOM간의 차이점을 발견하다고 하였다.

이때, key 값을 토대로 특정 노드의 자식 노드들 중에서 변경된 **(삭제, 추가)** 노드는 무엇인지 판단한다.


### key값을 index로 사용하면 안되는 이유

- 이유 알아보기
    
    아래와 같은 코드가 있다고 가정해보자.
    
    ```html
    // Index를 Key로 사용
    <ul>
      <li key="0">first</li>
      <li key="1">second</li>
      <li key="2">third</li>
    </ul>
    ```
    
    만약, 개발자가 가운데 `second` 를 가진 list ListElement를 삭제하는 버튼을 눌렀다고 가정해보자.
    
    아래와 같이 되기를 기대할 것이다.
    
    ```html
    // Index를 Key로 사용
    <ul>
      <li key="0">first</li>
      <li key="1">third</li>
    </ul>
    ```
    
    하지만, 실제로는 아래와 같이 된다.
    
    ```html
    // Index를 Key로 사용
    <ul>
      <li key="0">first</li>
      <li key="1">Second</li>
    </ul>
    ```
    
    이를 자세히 살펴보자.
    
    아래와 같이 기존 DOM에서 `key = “1”` 에 해당하는 list를 삭제하면 아래의 **State-Changed Virtual DOM**이  탄생한다.
    
    이때, 바뀐 배열로 인해 `key` 값은 third가 `key = “1”`을 차지하게 됨을 명심하자.
    
    이후, Reconciler는 key값을 토대로 바뀐 Element는 무엇인지 판단한다.
    
    key = “2” 가 사라졌으므로, 이를 Reconciler는 “key = “2”를 빼고 렌더링하면 되겠다” 고 Renderer로 전달하여 Renderer는 이를 렌더링한다.
    
    ```html
    // 기존 DOM
    <ul>
      <li key="0">first</li>
      <li key="1">second</li>
      <li key="2">third</li>
    </ul>
    
    // State-Changed Virtual DOM
    <ul>
      <li key="0">first</li>
      <li key="1">third</li>
    </ul>
    ```
    
    ### 또한, 리액트는 첫번째 노드부터 시작하여 변경사항을 추적한다.
    
    만약, 배열의 첫번째 요소에 값이 추가되면 리액트는 모든 요소를 재렌더링해야 한다.
    
    ```jsx
    <ul>
      <li key="0">Duke</li>
      <li key="1">Villanova</li>
    </ul>
    
    <!-- key가 0인 자식 엘리먼트를 처음에 추가. 오직 0만 재렌더링된다. -->
    <ul>
      <li key="0">Connecticut</li>
      <li key="1">Duke</li>
      <li key="2">Villanova</li>
    </ul>
    ```
    
    하지만, key에 id 값을 사용하면 추가된 요소만 재렌더링하면 된다.
    
    ```jsx
    <ul>
      <li key="2021">Duke</li>
      <li key="2022">Villanova</li>
    </ul>
    
    <!-- key가 2020인 자식 엘리먼트를 처음에 추가. 오직 2020만 재렌더링된다. -->
    <ul>
      <li key="2020">Connecticut</li>
      <li key="2021">Duke</li>
      <li key="2022">Villanova</li>
    </ul>
    ```
    

    ### key에 올바른 값을 사용하기
    
    많은 개발자들이 염두하고 있듯이 key 값에는 값을 구분할 수 있는 고유의 값을 사용하자.
    
    서버에서 제공받는 데이터라면, 대부분 id 값을 토대로 구분할 수 있다.
    
    혹여나 index를 사용해야 한다면, **변하지 않는 정적 데이터에만 사용**하자.
    
    ```jsx
    const navBarList = (
      <ul>
        {Array.from({ length: 3 }, (_, index) => (
          <li key={index}>이동하기 ${index}</li>
        ))}
      </ul>
    )
    
    <ul>
    	<li key="1">
    	<li key="2">
    	<li key="3">
    </ul>
    ```
    



### Virtual DOM 개발 시 고려해야 하는 점

[리액트 Virtual Dom 생성방법 아티클](https://medium.com/@gethylgeorge/how-virtual-dom-and-diffing-works-in-react-6fc805f9f84e)

1. Marking the Component(Node) Dirty (변경사항 알아차리기)
    
    변경사항이 있는 컴포넌트는 Dirty 상태로 저장한다.
    
    ```jsx
    dirtyComponents.push(component);
    ```
    
2. Dirty 상태를 마킹하는 방법
    - `if(HTML 엘리먼트 타입이 다른 경우)`
        
        하위 자식을 포함한 모든 노드를 Dirty 상태로 마킹하여 재렌더링을 유도한다.
        
        ```jsx
        // 이전
        <div>{children}</div>
        
        // 이후
        <span>{children}</span>
        ```
        
    - `else if(속성이 다른 경우)`
        
        두 엘리먼트의 속성을 비교하여, 동일한 내역을 유지하고 변경된 속성만 갱신한다.
        
    - 이후, 자식 요소를 재귀적으로 처리한다.

3. Patch 알고리즘 (변경사항을 실제 노드에 반영하는 알고리즘)
    
    고려해야 하는 점
    
    - 상태 변경사항을 추적
    - (Ref) 변경사항 추적
    
    <img width="553" alt="image" src="https://github.com/user-attachments/assets/7d7ca7f6-8328-4f6a-8884-763090220ced" />
