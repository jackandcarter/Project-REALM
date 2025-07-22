using System.Collections.Generic;
using Digger.Modules.Core.Sources;
using Digger.Modules.Runtime.Sources;
using UnityEngine;
using UnityEngine.UI;

public class RuntimeTerrainEditor : MonoBehaviour
{
    [Header("Digger Master Runtime")]
    [SerializeField] private DiggerMasterRuntime diggerMasterRuntime;

    [Header("UI Elements")]
    [SerializeField] private Dropdown brushDropdown;
    [SerializeField] private Dropdown actionDropdown;
    [SerializeField] private Slider sizeSlider;

    private void Awake()
    {
        if (!diggerMasterRuntime)
        {
            diggerMasterRuntime = FindObjectOfType<DiggerMasterRuntime>();
        }

        PopulateDropdown(brushDropdown, typeof(BrushType));
        PopulateDropdown(actionDropdown, typeof(ActionType));
    }

    private static void PopulateDropdown(Dropdown dropdown, System.Type enumType)
    {
        if (dropdown == null)
            return;

        dropdown.ClearOptions();
        dropdown.AddOptions(new List<string>(System.Enum.GetNames(enumType)));
        dropdown.value = 0;
    }

    public void OnBrushChanged(int index)
    {
        // Method kept for Unity UI events
    }

    public void OnActionChanged(int index)
    {
        // Method kept for Unity UI events
    }

    public void OnSizeChanged(float value)
    {
        // Method kept for Unity UI events
    }

    private BrushType SelectedBrush => brushDropdown ? (BrushType)brushDropdown.value : BrushType.Sphere;
    private ActionType SelectedAction => actionDropdown ? (ActionType)actionDropdown.value : ActionType.Dig;
    private float SelectedSize => sizeSlider ? sizeSlider.value : 4f;

    private void Update()
    {
        if (!diggerMasterRuntime)
            return;

        if (Input.GetMouseButton(0))
        {
            if (Physics.Raycast(transform.position, transform.forward, out var hit, 2000f))
            {
                diggerMasterRuntime.ModifyAsyncBuffured(hit.point, SelectedBrush, SelectedAction, 0, 0.5f, SelectedSize);
            }
        }
    }
}
