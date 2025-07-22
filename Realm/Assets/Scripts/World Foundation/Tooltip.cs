using UnityEngine;
using TMPro;

public class Tooltip : MonoBehaviour
{
    [Header("UI Elements")]
    [SerializeField] private TMP_Text tooltipText; // Reference to the TMP_Text component
    [SerializeField] private RectTransform backgroundRect; // Tooltip background

    [Header("Appearance Settings")]
    public Vector2 padding = new Vector2(10f, 10f); // Padding for text

    public void SetText(string text)
    {
        if (tooltipText == null || backgroundRect == null)
        {
            Debug.LogError("Tooltip components are not assigned!");
            return;
        }

        // Set the text
        tooltipText.text = text;

        // Adjust the background size based on the text
        Vector2 textSize = tooltipText.GetPreferredValues(text);
        backgroundRect.sizeDelta = textSize + padding;
    }
}
