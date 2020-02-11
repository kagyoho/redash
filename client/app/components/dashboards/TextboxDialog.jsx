import { markdown } from 'markdown';
import { debounce } from 'lodash';
import React from 'react';
import PropTypes from 'prop-types';
import Modal from 'antd/lib/modal';
import Input from 'antd/lib/input';
import Tooltip from 'antd/lib/tooltip';
import Divider from 'antd/lib/divider';
import HtmlContent from '@/components/HtmlContent';
import { wrap as wrapDialog, DialogPropType } from '@/components/DialogWrapper';
import notification from '@/services/notification';

import './TextboxDialog.less';

class TextboxDialog extends React.Component {
  static propTypes = {
    dashboard: PropTypes.object.isRequired, // eslint-disable-line react/forbid-prop-types
    dialog: DialogPropType.isRequired,
    onConfirm: PropTypes.func.isRequired,
    text: PropTypes.string,
  };

  static defaultProps = {
    text: '',
  };

  updatePreview = debounce(() => {
    const text = this.state.text;
    this.setState({
      preview: markdown.toHTML(text),
    });
  }, 100);

  constructor(props) {
    super(props);
    const { text } = props;
    this.state = {
      saveInProgress: false,
      text,
      preview: markdown.toHTML(text),
    };
  }

  onTextChanged = (event) => {
    this.setState({ text: event.target.value });
    this.updatePreview();
  };

  saveWidget() {
    this.setState({ saveInProgress: true });

    this.props.onConfirm(this.state.text)
      .then(() => {
        this.props.dialog.close();
      })
      .catch(() => {
        notification.error('Widget could not be added');
      })
      .finally(() => {
        this.setState({ saveInProgress: false });
      });
  }

  render() {
    const { dialog } = this.props;
    const isNew = !this.props.text;

    return (
      <Modal
        {...dialog.props}
        title={isNew ? '添加文本框' : '编辑文本框'}
        onOk={() => this.saveWidget()}
        okButtonProps={{
          loading: this.state.saveInProgress,
          disabled: !this.state.text,
        }}
        okText={isNew ? '添加到看板' : '保存'}
        cancelText="取消"
        width={500}
        wrapProps={{ 'data-test': 'TextboxDialog' }}
      >
        <div className="textbox-dialog">
          <Input.TextArea
            className="resize-vertical"
            rows="5"
            value={this.state.text}
            onChange={this.onTextChanged}
            autoFocus
            placeholder="在这里写一些文字"
          />
          <small>
            支持基于{' '}
            <a
              target="_blank"
              rel="noopener noreferrer"
              href="https://www.markdownguide.org/cheat-sheet/#basic-syntax"
            >
              <Tooltip title="在新窗口中打开Markdown指南">Markdown</Tooltip>
            </a>标记语言。
          </small>
          {this.state.text && (
            <React.Fragment>
              <Divider dashed />
              <strong className="preview-title">预览：</strong>
              <HtmlContent className="preview markdown">{this.state.preview}</HtmlContent>
            </React.Fragment>
          )}
        </div>
      </Modal>
    );
  }
}

export default wrapDialog(TextboxDialog);
