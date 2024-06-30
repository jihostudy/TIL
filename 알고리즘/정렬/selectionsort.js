// 선택정렬
function selectionsort(arr) {
  let i, j, min;
  const len = arr.length;
  for (i = 0; i < len; i++) {
    min = i;
    for (j = i + 1; j < len; j++) {
      if (arr[min] > arr[j]) {
        min = j;
      }
    }
    // 구조분해할당으로 SWAP
    [arr[i], arr[min]] = [arr[min], arr[i]];
  }
  return arr;
}

// const arr = [3, 4, 1, 2, 7];
// console.log(selectionsort(arr));
