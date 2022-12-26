#include "mainwindow.h"
#include "./ui_mainwindow.h"
#include <math.h>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    QPixmap pixmap("/home/tehnokrat/CLionProjects/SInkometr/resources/reload_better.png");
    QIcon ButtonIcon(pixmap);
    ui->pushButton->setIcon(ButtonIcon);
    ui->pushButton->setIconSize(pixmap.rect().size());

    ui->plot->addGraph(); // temperature
    ui->plot->graph(0)->setPen(QColorConstants::Red);

    ui->plot->addGraph(); // humadity
    ui->plot->graph(1)->setPen(QColorConstants::Cyan);


    ui->plot->addGraph(); // pressure
    ui->plot->graph(2)->setPen(QColorConstants::Yellow);



    //ui->plot->graph(0)->setScatterStyle(QCPScatterStyle::ssCircle);
    //ui->plot->graph(0)->setLineStyle(QCPGraph::lsLine);

    socket = new QTcpSocket();

}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::add_point(double x, double y, int plot_number){
    qv_x.append(x);
    switch(plot_number){
    case 0:
        qv_yt.append(y);
        break;
    case 1:
        qv_yh.append(y);
        break;
    case 2:
        qv_yp.append(y);
        break;
    }
}


void MainWindow::clear_data(){

    qv_x.clear();
    qv_yt.clear();
    qv_yh.clear();
    qv_yp.clear();
    qDebug()<<ui->comboBox->count();
    for (int i =0; i < ui->comboBox->count() ; i++){
        plot(i);
    }
}

void MainWindow::plot(int number_plot){
    QVector <double> qv_y;
    switch(number_plot){
    case 0:
        qv_y = qv_yt;
        break;
    case 1:
        qv_y = qv_yh;
        break;
    case 2:
        qv_y = qv_yp;
        break;
    }
    ui->plot->graph(number_plot)->setData(qv_x, qv_y);
    ui->plot->graph(number_plot)->rescaleAxes(true);
    ui->plot->replot();
    ui->plot->update();
}

void MainWindow::on_pushButton_clicked(){

    socket->connectToHost("192.168.4.1", 80);

    if(socket->waitForConnected(3000)){
        qDebug() << "Connected!";

        // send
        socket->write("need_all");
        socket->waitForBytesWritten(1000);
        socket->waitForReadyRead(3000);
        qDebug() << "Reading: " << socket->bytesAvailable();
        QByteArray result = socket->readAll();

        qDebug()<<QString::fromLocal8Bit(result);
        ui->textBrowser->append(QString::fromLocal8Bit(result));
        socket->close();
    }
    else
    {
        qDebug() << "Not connected!";
    }
}



void MainWindow::on_comboBox_currentIndexChanged(int index)
{
//    clear_data();
//    ui->textBrowser->append(QString::number(index));
//    for (int i=0; i<100; i++){
//        add_point(i, tan(i)*180/3.14);
//    }
//    plot(index);
}


void MainWindow::on_comboBox_textActivated(const QString &arg1)
{
    clear_data();
    ui->textBrowser->append(arg1);
    if (arg1 == "temperature"){
        for (int i=0; i<100; i++){
            add_point(i, tan(i)*180/3.14, (int) ui->comboBox->currentIndex());
        }
    }
    if (arg1 == "humadity"){
        for (int i=0; i<100; i++){
            add_point(i, cos(i)*180/3.14, (int) ui->comboBox->currentIndex());
        }
    }
    if (arg1=="pressure"){
        for (int i=0; i<100; i++){
            add_point(i, sin(i)*180/3.14, (int) ui->comboBox->currentIndex());
        }
    }
    plot((int) ui->comboBox->currentIndex());
}

