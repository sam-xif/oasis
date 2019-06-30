import React from 'react';
import {Modal, Button} from 'react-bootstrap';

export class ProjectModal extends React.Component {
  render() {
    const {name, description, lifecycle, onHide} = this.props;
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
