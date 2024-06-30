// 버블정렬 (오름차순)
function bubblesort(arr) {
  let i, j;
  const len = arr.length;
  for (i = 0; i < len; i++) {
    for (j = 0; j < len - i - 1; j++) {
      if (arr[j] > arr[j + 1]) {
        [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
      }
    }
    // 구조분해할당으로 SWAP
  }
  return arr;
}

const arr = [11, 3, 4, 1, 2, 7];
console.log(bubblesort(arr));
