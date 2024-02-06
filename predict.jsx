import React, { Component } from 'react';
import ApiService from "../service/ApiService";
import {Route, Link, Routes, useParams} from 'react-router-dom';
import plus from './home.png';

function Users() {
    // 👇️ get ID from url
    const params = useParams();
  
    console.log(params); // 👉️ {userId: '4200'}
  
    return params.id;
  }

class PredictionPage extends Component {
    constructor(props){
        super(props);
        this.state = {
            id: null,
            predict_img: null,
            dspl_img: null,
            dragActive: false,
            predictions:[],
            showRes: false,
            plotData: '', // Add this new state variable
            period: '1', // default period
            currency: 'BTC' // default currency
        }
        //this.reloadModelList = this.reloadModelList.bind(this);
        this.fetchPlotData = this.fetchPlotData.bind(this)
        this.handleSelectChange = this.handleSelectChange.bind(this)
    }

    

    fetchPlotData = () => {
        fetch('http://localhost:5000/get-plot') // Adjust URL as needed
            .then(response => response.json())
            .then(data => {
                this.setState({ plotData: `data:image/png;base64,${data.plot_url}` });
            })
            .catch(error => console.error('Error fetching plot:', error));
    }

    handleSelectChange = (event) => {
        this.setState({ [event.target.name]: event.target.value });
    }
        

    predict(){
        //fetchPlotData();
        let id = window.location.href.split('/')[4];
        console.log(id);
        let predictDetails = {
            period: this.state.period,
            currency: this.state.currency,
            id: id
        };
        const predictData = new FormData()
        predictData.append('id', id);
        predictData.append('period', this.state.period);
        predictData.append('currency', this.state.currency);
        predictData.append('id', id);

        alert("Started prediction");
        ApiService.predict(predictData)
            .then(res => {
                this.setState({showRes: true});
                this.setState({ plotData: `data:image/png;base64,${res.data.plot_url}` });
               if( res.data=='')
               {
                alert("wrong");
               }
               else {
                alert("Prediction results are ready");
               }
            })
    }



render(idd) {
    return (
        <div className="cont">
            <div className='header_home'>
                <div><h2 className="text_header">Predict</h2></div>
                <div><a href='/' className="btn_home"><img alt="Home" src={plus}></img></a></div>
            </div>
            <div className="select-container">
                <label htmlFor="period-select">Select Period:</label>
                <select id="period-select" name="period" value={this.state.period} onChange={this.handleSelectChange}>
                    {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(day => (
                        <option key={day} value={day}>{day} day(s)</option>
                    ))}
                </select>
                <label htmlFor="currency-select">Select Currency:</label>
                <select id="currency-select" name="currency" value={this.state.currency} onChange={this.handleSelectChange}>
                    {['KSN', 'CMP', 'XRP'].map(currency => (
                        <option key={currency} value={currency}>{currency}</option>
                    ))}
                </select>
            </div>
            {!this.state.showRes && (
                <div className="btns">
                    <button className="btn btn-success" onClick={() => this.predict(this.state.img)}>Predict</button>
                </div>
            )}
            {this.state.showRes && this.state.plotData ? (
                <div className="plot-container">
                    <img src={this.state.plotData} alt="Plot" />
                </div>
            ):""}
        </div>
    );
}
}

export default PredictionPage;

