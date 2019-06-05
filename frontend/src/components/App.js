import React from 'react';
import '../styles/App.css';
import {Card, Button, Modal} from 'react-bootstrap'
import {client} from '../index.js'
import { Query } from 'react-apollo'
import gql from 'graphql-tag'



const projectsQuery = gql`
  {
      project {
          id
          name
          description
          lifecycle
      }
  }
`



class ProjectTableElement extends React.Component {
  render() {
    const {id, name, description, showProject} = this.props

    return <Card>
      <Card.Header>Featured</Card.Header>
      <Card.Body>
        <Card.Title>{name}</Card.Title>
        <Card.Text>
          {description}
        </Card.Text>
        <Button variant="primary" value={id} onClick={ showProject}>Show Project</Button>
      </Card.Body>
    </Card>
  }
}

class Project extends React.Component {
  render() {
    const {name, description, lifecycle, onHide} = this.props;
    console.log('went here');
    console.log(this.props);
    return <Modal
        {...this.props}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered>
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">
          {name}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <ul>
          <li>Description: {description}</li>
          <li>Lifecycle status: {lifecycle}</li>
        </ul>
      </Modal.Body>
      <Modal.Footer>
        <Button onClick={onHide}>Close</Button>
      </Modal.Footer>
    </Modal>
  }
}


class ProjectTable extends React.Component {
  state = {
    projects: [{id: 1, name: 'Some Cool Project', description: 'Description of some cool project', lifecycle: 'Prototype'},
      {id: 2, name: 'Some other one', description: 'Description of some other cool project', lifecycle: "Beta"},
      {id: 3, name: 'Some third one', description: 'Description of some third cool project', lifecycle: "Deployment"}],
    showProject: false,
    projectToShow: 1


  };




  componentDidMount() {
    console.log('fetching')

    client.query({
      query: gql`
        {
          project {
            id
            name
            description
            lifecycle
          }
        }
      `
    }).then(response => {
      console.log('Got data', response.data)
      this.setState({projects: response.data.project})
    });

    // <Query query={projectsQuery}>
    //   {({ loading, error, data }) => {
    //     if (loading) return "Loading...";
    //     if (error) return `Error! ${error.message}`;
    //     console.log("data: ", data);}}
    // </Query>
  }

  showProject = event => {
      const id = event.target.value;
      this.setState({showProject: true, projectToShow: id})
  };

  hideProject = () => {
    this.setState({showProject: false})
  };

  render() {
    const {projects, projectToShow, showProject} = this.state;

    const projectsRendered = projects.map(project => <ProjectTableElement id={project.id} name={project.name} description={project.description} showProject={this.showProject}> </ProjectTableElement>);
    const project = projects.find(el => {return el.id == projectToShow});
    const newProps = {...project, onHide: this.hideProject, show:showProject}
    const projectRendered = <Project {...newProps}/>;
    console.log({...newProps})
    //name={project.name} description={project.description} link={project.link} lifecycle={project.lifecycle}

    return (
        <div>
          {projectsRendered}
          {projectRendered}
        </div>
    );
  }

}

class App extends React.Component {
  render() {
    return <ProjectTable/>
  }
}

export default App;
