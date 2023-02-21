using UnityEngine;

/* Source: https://www.youtube.com/watch?v=zKRMkD28-xY&list=PLLf84Zj7U26kfPQ00JVI2nIoozuPkykDX&index=7
 * Who: Game Dev Experiments 
 * What: 2D Unity Pokemon Clone Tutorial
 * When: Feb 20, 2023
 * Why: I tried implementing a typed dialog box on my own, and couldn't get it right.
 * So I wanted to re-learn it from someone else. 
 */


public class TypedDialog : MonoBehaviour 
{    
    [SerializeField] TextMeshProUGUI dialogText;
    [SerializeField] int charactersPerSecond;

    private void Start() 
    {
        StartCoroutine(TypeDialog("Wow it's typing on its own... or is it"))
    }
    
    
    public IEnumerator TypeDialog(string dialog)
    {
        dialogText.text = "";
        foreach (var character in dialog.ToCharArray())
        {
            dialogText.text += character;
            yield return new WaitForSeconds(1f/charactersPerSecond);
        }
    }


}
