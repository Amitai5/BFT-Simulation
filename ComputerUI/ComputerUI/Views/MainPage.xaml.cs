using System.IO.Ports;

namespace ComputerUI.Views;

public partial class MainPage : ContentPage
{
    SerialPort ModelCOMPort;

    public MainPage()
    {
        InitializeComponent();

        ModelCOMPort = new SerialPort("COM3")
        {
            DtrEnable = true,
            RtsEnable = true,
            BaudRate = 9600
        };

        ModelCOMPort.DataReceived += SerialPort_DataReceived;
        ModelCOMPort.Open();
    }

    private void SerialPort_DataReceived(object sender, SerialDataReceivedEventArgs e)
    {
        string data = ModelCOMPort.ReadLine();
        double force = double.Parse(data[..data.IndexOf(';')]);

        Console.WriteLine("Force: " + force);
        Application.Current.MainPage.Dispatcher.Dispatch(() => UpdateForces(force));
    }

    private void ClearResultsBTN_Clicked(object sender, EventArgs e)
    {
        UpdateForces(0);
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
}