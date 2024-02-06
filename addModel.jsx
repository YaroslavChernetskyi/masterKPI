import React, { Component } from 'react';
import ApiService from "../service/ApiService";
import home from './home.png';
import plus from './plus.png';

class AddModel extends Component {
    constructor(props){
        super(props);
        this.state = {
            id: null,
            model_name: '',
            model_description: '',
            accuracy: '',  // New field
            data_type: '', // New field
            strategy: '',  // New field
            time_step: '',  // New field
            json_model: null,
            json_model_id: 0,
            json_name: '',
            json_description: '',
            model_weights_path: '',
            training_graphics_path: '',
            no_disease_precision: '',
            val_no_disease_precision: '',
            accuracy: '',
            val_accuracy: '',
            metadata: null,
            classId:0,
            classElem: '',
            classes: [],

            image: null,
            models: [],
            model_to_show: ''
        }
        this.saveModel = this.saveModel.bind(this);
        this.reloadModelList = this.reloadModelList.bind(this);
    }

componentDidMount() {
    this.reloadModelList();
}

reloadModelList() {
    // ApiService.fetchModels()
    //     .then((res) => {
    //         this.setState({models: res.data})
    //     });
    ApiService.getAddModel()
        .then((res) => {
            this.setState({models: res.data})
        });
}

    saveModel = (e) => {
        
        e.preventDefault();
        let model = {
            model_name: this.state.model_name,
            model_description: this.state.model_description,
            json_model_id: this.state.json_model_id,
            json_model: this.state.json_model,
            json_name: this.state.json_name
        };
        console.log(model);
        const formData = new FormData();
        formData.append('model_name', this.state.model_name);
        formData.append('model_description', this.state.model_description);
        formData.append('accuracy', this.state.accuracy); // New field
        formData.append('data_type', this.state.data_type); // New field
        formData.append('strategy', this.state.strategy); // New field
        formData.append('time_step', this.state.time_step); // New field
        formData.append('json_model_id', model.json_model_id);
        formData.append('json_model', this.state.json_model);
        formData.append('json_name', model.json_model.name);
        formData.append('json_description', this.state.json_description);
        console.log("Before req");
        for (let [key, value] of formData.entries()) {
            console.log(key, value);
        }
        ApiService.addModel(formData)
            .then(res => {
                window.location = '/';
            });
    }

    uploadJsonFile = (e) =>
        this.setState({json_model:e.target.files[0]});

    onChange = (e) =>{
        this.setState({ [e.target.name]: e.target.value });
    }
    onChange1 = (e) =>{
        this.setState({ [e.target.name]: e.target.value });
        this.state.models.forEach(el => {

            // alert(this.state.model_to_show);
            if(el.model_name == e.target.value)
            {
                let json_obj = this.state.models.filter(o => o.model_name == e.target.value)[0];
                this.state.json_name = json_obj.model_name;
                this.state.json_description = json_obj.model_description;
                this.state.json_model_id = json_obj.id;
            }
        });
    }

    render() {
        const items = [];

        this.state.models.filter(o => {items.push(<option id={o.id} value={o.model_name}/>)});

        return(
            <div>
                <div className='header_home'>
                    <div><h2 className="text_header">Add Model</h2></div>
                    <div><a href='/' className="btn_home"> <img alt="Home" src={home} ></img></a></div>
                </div>
                <div className='model_form'>
                <form>
                <div className="form-group">
                    <label>Model name:</label>
                    <input type="text" name="model_name" className="form-control" value={this.state.model_name} onChange={this.onChange}/>
                </div>

                <div className="form-group">
                    <label>Model description:</label>
                    <textarea name="model_description" cols="20" rows="5" value={this.state.model_description} onChange={this.onChange}></textarea>
                </div>

                <div className="form-group">
                <label>Accuracy:</label>
                <input type="text" name="accuracy" className="form-control" value={this.state.accuracy} onChange={this.onChange}/>
                </div>

                <div className="form-group">
                    <label>Data Type:</label>
                    <input type="text" name="data_type" className="form-control" value={this.state.data_type} onChange={this.onChange}/>
                </div>

                <div className="form-group">
                    <label>Strategy:</label>
                    <input type="text" name="strategy" className="form-control" value={this.state.strategy} onChange={this.onChange}/>
                </div>

                <div className="form-group">
                    <label>Time Step (minutes):</label>
                    <input type="number" name="time_step" className="form-control" value={this.state.time_step} onChange={this.onChange}/>
                </div>

                <div>
                        <label>Model JSON</label>	
                        <input className="file_input" type="file" name="json_model" onChange={this.uploadJsonFile}/>
                </div>

                

                <button className="btn btn-success" onClick={this.saveModel}>Save</button>
            </form>
                </div>
    </div>
        );
    }
}

export default AddModel;