using ComputerUI.Servies;

namespace ComputerUI.Views;

public partial class MainPage : ContentPage
{
    private ModelCOMService modelService;
    List<StackLayout> levels = new List<StackLayout>();

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
            SidePanelView.IsVisible = true;
        });
    }

    private void ModelConnectBTN_Clicked(object sender, EventArgs e)
    {
        ModelConnectBTN.IsVisible = false;
        ModelConnectBTN.VerticalOptions = LayoutOptions.End;

        LoadingLayout.IsVisible = true;
        LoadingLayout.VerticalOptions = LayoutOptions.CenterAndExpand;

        modelService.ConnectToModel();
    }

    private void UpdateForces(double force)
    {
        for (int i = 0; i < levels.Count; i++)
        {
            App.Current.Resources.TryGetValue("Gray", out object test);
            levels[i].BackgroundColor = (Color)test;
        }

        for (int i = 0; force > i * 25; i++)
        {
            App.Current.Resources.TryGetValue("Primary", out object test);
            levels[i].BackgroundColor = (Color)test;
        }

        if (force == 0)
        {
            PunchForceLBL.Text = "Equal to ## punches by a professional boxer";
            CarForceLBL.Text = "Equal to a car crashing at ## km/h";
            ForceLBL.Text = "Force: #### Newtons";
        }

        PunchForceLBL.Text = $"Equal to {Math.Round(force / 500)} punches by a professional boxer";
        CarForceLBL.Text = $"Equal to a car crashing at {Math.Round(force / 100)} km/h";
        ForceLBL.Text = $"Force: {Math.Round(force)} Newtons";
    }
}