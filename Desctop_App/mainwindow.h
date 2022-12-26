#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTcpSocket>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_pushButton_clicked();
    //void readFortune();
    //void errorMessage(QAbstractSocket::SocketError socketError);
    void add_point(double x, double y, int plot_number);
    void clear_data();
    void plot(int number_plot);

    //void on_pushButton_2_clicked();

    //void on_comboBox_currentIndexChanged(int index);

    void on_comboBox_textActivated(const QString &arg1);

private:
    Ui::MainWindow *ui;
    QTcpSocket *socket;
    QVector<double> qv_x, qv_yt, qv_yh, qv_yp;
    /*
     * qv_x -- time
     * qv_yt -- temperature
     * qv_yh -- humadity
     * qv_yp -- pressure
    */
};
#endif // MAINWINDOW_H
