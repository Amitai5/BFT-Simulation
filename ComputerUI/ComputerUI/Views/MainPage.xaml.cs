using ComputerUI.Servies;

namespace ComputerUI.Views;

public partial class MainPage : ContentPage
{
    private List<StackLayout> sidePanelViews = new List<StackLayout>();
    private List<StackLayout> levels = new List<StackLayout>();

    public const double BAR_SCALE_VALUE = 1847;
    private ModelCOMService modelService;

    public MainPage()
    {
        InitializeComponent();

        modelService = new ModelCOMService();
        modelService.OnConnected += Model_OnConnected;
        modelService.DataReceived += ModelService_DataReceived;

        levels.Add(Level1);
        levels.Add(Level2);
        levels.Add(Level3);
        levels.Add(Level4);
        levels.Add(Level5);
        levels.Add(Level6);

        sidePanelViews.Add(SidePanelView1);
        sidePanelViews.Add(SidePanelView2);
        sidePanelViews.Add(SidePanelView3);
        sidePanelViews.Add(SidePanelView4);
        sidePanelViews.Add(SidePanelView5);
        sidePanelViews.Add(SidePanelView6);
    }

    private void ModelService_DataReceived(double force)
    {
        Application.Current.MainPage.Dispatcher.Dispatch(() => UpdateForces(force));
    }

    private void Model_OnConnected()
    {
        Application.Current.MainPage.Dispatcher.Dispatch(() =>
        {
            LoadingView.IsVisible = false;
            SpacingFrame.IsVisible = true;
            ModelLegView.IsVisible = true;
            SidePanel.IsVisible = true;
        });
    }

    private void ModelConnectBTN_Clicked(object sender, EventArgs e)
    {
        ModelConnectBTN.IsVisible = false;
        ModelConnectBTN.VerticalOptions = LayoutOptions.End;

        LoadingLayout.IsVisible = true;
        LoadingLayout.VerticalOptions = LayoutOptions.CenterAndExpand;

        modelService.ConnectToModel();
        UpdateForces(0);
    }

    private void UpdateForces(double force)
    {
        for (int i = 0; i < levels.Count; i++)
        {
            App.Current.Resources.TryGetValue("Gray", out object test);
            levels[i].BackgroundColor = (Color)test;
            sidePanelViews[i].IsVisible = false;
        }

        int index = 0;
        for (; index < levels.Count && force > index * BAR_SCALE_VALUE; index++)
        {
            App.Current.Resources.TryGetValue("Primary", out object test);
            levels[index].BackgroundColor = (Color)test;
        }

        // Set the side panel
        if (index >= 1)
        {
            sidePanelViews[index - 1].IsVisible = true;
        }

        if (force == 0)
        {
            ForceLBL.Text = "Force: #### Newtons";
        }
        ForceLBL.Text = $"Force: {Math.Round(force)} Newtons";
    }
}