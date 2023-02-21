using UnityEngine;
using Random = UnityEngine.Random;

/*
 * Source:https://www.youtube.com/watch?v=h3EZ9G0Gtx0&list=PLLf84Zj7U26kfPQ00JVI2nIoozuPkykDX&index=6
 * Who: Game Dev Experiments Tutorial  
 * What: 2D Unity Pokemon Clone Tutorial
 * When: Feb. 19, 2023
 * Why: I haven't built a 2D game in a while, 
 * and picked this tutorial to get back into the pace of things.
 */

public class PlayerController : MonoBehaviour
{
    public LayerMask solidObjectsLayer;
    public LayerMask grassLayer;

    public float moveSpeed;
    private bool isMoving;
    private Vector2 input;

    if(!isMoving)
    {
        input.x = Input.GetAxisRaw("Horizontal"); // get axis raw always returns [-1, 1]
        input.y = Input.GetAxisRaw("Vertical");
        
        if (input.x != 0) input.y = 0; // remove diagonal movement

        if (input != Vector2.zero)
        {
            animator.SetFloat("moveX", input.x);
            animator.SetFloat("moveY", input.y);

            var targetPos = transform.position;
            targetPos.x += input.x;
            targetPos.y += input.y;
            if (IsWalkable(targetPos)) 
            {
                StartCoroutine(Move(targetPos));
            }
        }
    }

    IEnumerator Move(Vector3 targetPos)
    {
        isMoving = true;
        // what is sqrMagnitude.
        while ((targetPos - transform.position).sqrMagnitude > Mathf.Epsilon)
        {
            transform.position = Vector3.MoveTowards(transform.position, targetPos, moveSpeed * Time.deltaTime);
            yield return null; // this stops the execution of the coroutine, and resume at the next update call
        }
        transform.position = targetPos;
        isMoving = false;

        CheckForEncounters();
    }

    private void CheckForEncounters()
    {
        // grass walking collisions don't work. 
        if (Physics2D.OverlapCircle(transform.position, 0.2f, grassLayer) != null)
        {
            Debug.Log("Walking on grass");
            if(Random.Range(1, 101) <= 10)
            {
                Debug.Log("Encountered a wild pokemon");
            }
        }
    }

    private bool IsWalkable(Vector3 targetPos)
    {
        if(Physics2D.OverlapCircle(targetPos, 0.2f, solidObjectsLayer) != null)
        {
            return false;
        }
        return true;
    }
}