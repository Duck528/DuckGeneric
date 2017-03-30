
import math


def init(arr, tree, node, start, end):
    """
    입력된 arr 배열의 값을 통해 세그먼트 트리의 정의를 만족하는 배열을 tree 배열에 할당한다
    :param arr: 사용자가 입력한 값의 배열
    :param tree: 세그먼트 트리의 정의를 만족하는 배열 (arr 배열의 구간 합)
    :param node: 재귀적으로 코드가 진행되므로 현재 값을 할당하는 tree 배열의 인덱스를 나타낸다
    :param start: 세그먼트 트리의 구간 중 시작 부분
    :param end: 세그먼트 트리의 구간 중 끝 부분
    :return: 가장 마지막에 리턴되는 값은 세그먼트 트리의 루트 노드의 값
    : 주의할 점은 세그먼트 트리 tree 배열의 루트 노드는 인덱스 1번에 위치한다는 점을 주의하자
    """
    # 세그먼트 트리의 단말 노드인 경우엔 단순히 값만 삽입한다
    if start == end:
        tree[node] = arr[start]
        return tree[node]

    # 단말 노드가 아니라면 자식 노드로 재귀적으로 진행한다
    # 세그먼트 트리의 예제를 자식 노드는 다음과 같음을 알 수 있다
    # 왼쪽 자식의 범위: [start ~ (end/2)]
    # 오른쪽 자식의 범위: [((end/2)+1) ~ end]
    # 아래의 코드는 그 범위를 지정해 주는 코드이다
    mid = math.trunc((start + end) / 2)

    # 재귀적으로 값을 더하며 현재 노드의 값을 결정한다 (Bottom up 방식)
    # 세그먼트 트리의 왼쪽 트리의 총 합
    sum_left_child_tree = init(arr, tree, node*2, start, mid)
    # 세그먼트 트리의 오른쪽 트리의 총 합
    sum_right_child_tree = init(arr, tree, node*2+1, mid+1, end)
    # 현재 노드의 값은 왼쪽 서브 트리의 총합 + 오른쪽 서브 트리의 총 합이 된다
    tree[node] = sum_left_child_tree + sum_right_child_tree
    print(tree[node], " node: ", node)
    return tree[node]


def update(tree, node, start, end, index, diff):
    # 변경된 노드의 범위를 벗어났다면 더 이상 갱신을 진행하지 않도록 방지하는 코드
    if index < start or index > end:
        return

    # 현재 노드에서 변경된 값의 차이를 더해준다
    tree[node] += diff

    # 트리의 단말 노드가 아니라면
    if start != end:
        mid = (start + end) / 2
        # 현재 노드의 왼쪽 자식 노드로 이동한다
        update(tree, node*2, start, mid, index, diff)
        # 현재 노드의 오른족 자식 노드로 이동한다
        update(tree, node*2+1, mid+1, end, index, diff)


def sum(tree, node, start, end, left, right):
    """
    세그먼트 트리의 합을 구하는 과정은 다음 4가지 경우가 존재한다
    1. [left, right]와 [start, end]가 겹치지 않는 경우
    : 구간 합을 구하고자 하는 범위와 상관이 없는 경우를 말한다
    2. [left, right]와 [start, end]를 완전히 포함하는 경우
    : 구하고자 하는 구간 합 구간에 포함되는 경우
    3. [start, end]가 [left, right]를 완전히 포함하는 경우
    : 구하고자 하는 구간 합 범위보다 크게 있지만 그 내부에 구하고자 하는 구간 합 범위가 있는 경우
    4. [left, right]와 [start, end]가 겹쳐져 있는 경우
    : (1, 2, 3)을 제외한 나머지 경우이며
    : left <= start <= right <= end 와 같은 방식을 말한다
    :param tree: 세그먼트 트리의 조건을 만족하는 1차원 배열
    :param node: 재귀호출로 진행되므로 세그먼트 트리의 현재 작업중인 노드 번호
    :param start: 현재 작업중인 세그먼트 트리 노드의 시작 값
    :param end: 현재 작업중인 세그먼트 트리 노드의 끝 값
    :param left: 구하고자 하는 구간 합의 시작 범위
    :param right: 구하고자 하는 구간 합의 끝 범위
    :return: 마지막 리턴 값은 left ~ right 구간의 합이 된다
    """
    if left > end or right < start:
        return 0

    if left <= start and end <= right:
        return tree[node]

    mid = (start + end) / 2
    # 왼쪽 서브 트리의 구간 합
    sum_left_child_tree = sum(tree, node*2, start, mid, left, right)
    # 오른쪽 서브 트리의 구간 합
    sum_right_child_tree = sum(tree, node*2+1, mid+1, end, left, right)
    return sum_left_child_tree + sum_right_child_tree


values = [3, 5, 6, 7, 2, 9, 4, 5, 2, 8, 1, 5]
segment_tree_height = math.ceil(math.log(len(values), 2)) + 1
num_terminal = (1 << segment_tree_height)
tree = [0 for i in range(num_terminal)]

init(values, tree, 1, 0, len(values)-1)
print(tree)
