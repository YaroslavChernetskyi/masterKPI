import React, { Component } from 'react';
import ApiService from "../service/ApiService";
import home from './home.png';
import { Link } from 'react-router-dom';

class ModelToShow extends Component {
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
        let model_name = model.model_name,
        model_description = model.model_description,
        /*json_model = model.json_model,
        model_weights_path = model.model_weights_path,
        training_graphics_path = model.training_graphics_path,*/
        no_disease_precision = model.no_disease_precision,
        val_no_disease_precision = model.val_no_disease_precision,
        accuracy = model.accuracy,
        val_accuracy = model.val_accuracy,
        training_metadata = model.training_metadata,
        //completeness = model.completeness,*/
        classes = ["Atelectasis", "Cardiomegaly", "Consolidation", "Covid",
            "Effusion", "Emphysema", "Infiltration", "Mass", "NoFinding",
            "Mass", "PleuralThickening", "Pneumothorax"];

        let class_string = '';

        for (let i of classes) {
            class_string += class_string ? (', ' +i) :  i;
        }
        return (
            <div className='model_info'>
                <div className="charact">
                    <label>Model name:</label>
                    <div>{model_name} </div>
                </div>
                <div className="charact">
                    <label>Model description:</label><br/>
                    <div>{model_description} </div>
                </div>
                <div className="charact">
                    <label>No Disease Precision:</label><br/>
                    <div>{no_disease_precision} </div>
                </div>
                <div className="charact">
                    <label>Validation No Disease Precision:</label><br/>
                    <div>{val_no_disease_precision} </div>
                </div>
                <div className="charact">
                    <label>Accuracy:</label><br/>
                    <div>{accuracy} </div>
                </div>
                <div className="charact">
                    <label>Validation accuracy:</label><br/>
                    <div>{val_accuracy} </div>
                </div>
                <div className="charact">
                    <label>Classes:</label><br/>
                    <div>{class_string} </div>
                </div>
                <div className="charact">
                    <label>Training Metadata:</label><br/>
                    <div><a href={training_metadata}>Download</a></div>
                </div>
            </div>
        );
    }

    renderModels() {
        let model_id = window.location.href.split('/')[4];
        let res = [];
        if (this.state.models!=null) {
            for (let i of this.state.models) {
                console.log(i.id);
                if(i.id == model_id)
                {
                    res.push(this.renderAllData(i));
                    break;
                }

            }
        }

        return res;
    }

    render() {
        return (
            <div>
                <div className='header_home'>
                    <div><h2 className="text_header">Model</h2></div>
                    <div><a href='/' className="btn_home"> <img alt="Home" src={home} ></img></a></div>
                </div>
                    {this.renderModels()}
            </div>
        );
    }
}

export default ModelToShow;

