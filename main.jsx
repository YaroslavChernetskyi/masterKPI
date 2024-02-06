import React, { Component } from 'react';
import ApiService from "../service/ApiService";
import plus from './plus.png';
import { Link } from 'react-router-dom';

class Models extends Component {
    constructor(props){
        super(props);
        this.state = {
            id: null,
            models: []
        }
        this.reloadModelList = this.reloadModelList.bind(this);
    }

    componentDidMount() {
        this.reloadModelList();
    }

    reloadModelList() {
        ApiService.fetchModels()
            .then((res) => {
                this.setState({models: res.data})
            });
    }

    renderAllData(model) {
            let id = model.id, 
            model_name = model.model_name,
            model_description = model.model_description,
            json_model = model.json_model,
            accuracy = model.accuracy,
            data_type = model.data_type, // New field
            strategy = model.strategy, // New field
            time_step = model.time_step; // New field

            console.log(json_model);
        return (
            <tr>
                <td>{ model_name}</td>
                <td>{ json_model.model_name}</td>
                <td>{ model_description }</td>
                <td>{ accuracy }</td>
                <td>{ data_type }</td> 
                <td>{ strategy }</td>
                <td>{ time_step }</td>
                <td>
                    <Link to={`/predict/${id}`} >Predict</Link>
                </td>
            </tr>
        );
    }

    renderModels() {
        let res = [];
        if (this.state.models!=null) {
            for (let i of this.state.models) {
                res.push(this.renderAllData(i));
            }
        }
        return res;
    }
    render() {
        return (
            <div>
                <div className='header_home'>
                    <div><h2 className="text_header">Training models</h2></div>
                    <div><a href='/create' className="btn_home"> <img alt="Add Model" src={plus} ></img></a></div>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>Model name</th>
                            <th>Model JSON</th>
                            <th>Model Description</th>
                            <th>Accuracy</th>
                            <th>Data Type</th> 
                            <th>Strategy</th> 
                            <th>Time Step (minutes)</th> 
                            <th>Predict</th>
                        </tr>
                    </thead>
                    <tbody>
                        {this.renderModels()}
                    </tbody>
                </table>
            </div>
        );
    }
}

export default Models;

