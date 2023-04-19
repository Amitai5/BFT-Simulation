using ComputerUI.Servies;

namespace ComputerUI.Views;

public partial class MainPage : ContentPage
{
    private ModelCOMService modelService;

    public MainPage()
    {
        InitializeComponent();

        modelService = new ModelCOMService();
        modelService.OnConnected += Model_OnConnected;
        modelService.DataReceived += ModelService_DataReceived;
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
        if (force == 0)
        {
            ModelImage.Source = ImageSource.FromFile("model_leg.png");
            PunchForceLBL.Text = "Equal to ## punches by a professional boxer";
            CarForceLBL.Text = "Equal to a car crashing at ## km/h";
            ForceLBL.Text = "Force: #### Newtons";
            return;
        }

        ModelImage.Source = ImageSource.FromFile("model_leg_hit.png");
        PunchForceLBL.Text = $"Equal to {Math.Round(force / 500)} punches by a professional boxer";
        CarForceLBL.Text = $"Equal to a car crashing at {Math.Round(force / 100)} km/h";
        ForceLBL.Text = $"Force: {Math.Round(force)} Newtons";
    }

    private void ClearResultsBTN_Clicked(object sender, EventArgs e)
    {
        UpdateForces(0);
    }
}