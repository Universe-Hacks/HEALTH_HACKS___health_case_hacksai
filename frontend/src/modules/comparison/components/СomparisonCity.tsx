import {Button, Layout, Table} from "antd";
import type {ColumnsType} from 'antd/es/table';

function ComparisonCity() {

  interface DataType {
    key: string;
    name: string;
    address: string;
  }

  const {Header, Footer, Content} = Layout;

  const columns: ColumnsType<DataType> = [
    {
      title: 'Метрика / Город',
      dataIndex: 'name',
      key: 'name',
      render: (text) => <a>{text}</a>,
    },
    {
      title: 'Город 1',
      dataIndex: 'age',
      key: 'age',
    },
    {
      title: 'Город 2',
      dataIndex: 'address',
      key: 'address',
    },
    {
      title: 'Город 3',
      key: 'tags',
      dataIndex: 'tags',
    },
  ];

  const headerStyle: React.CSSProperties = {
    textAlign: 'left',
    display: 'flex',
    alignItems: 'center',
    color: '#fff',
    height: 100,
    paddingInline: 50,
    lineHeight: '64px',
    backgroundColor: '#eaeeef',
  };

  const contentStyle: React.CSSProperties = {
    textAlign: 'center',
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    lineHeight: '120px',
    paddingInline: 50,
    color: '#fff',
    width: '100%',
    backgroundColor: '#eaeeef',
  };

  const footerStyle: React.CSSProperties = {
    textAlign: 'center',
    color: '#fff',
    backgroundColor: '#eaeeef',
  };

  const data: DataType[] = [
    {
      key: '1',
      name: 'Метрика 1',
      address: '',
    },
    {
      key: '2',
      name: 'Метрика 2',
      address: '',
    },
    {
      key: '3',
      name: 'Метрика 3',
      address: '',
    },
  ];

  return (
    <Layout>
      <Header style={headerStyle}>
        <Button
          style={{
            backgroundColor: '#48773C',
            color: '#fff',
            display: 'inline-flex',
            alignItems: 'center',
            height: '48px',
            marginLeft: '40px',
            textDecoration: 'none',
            borderRadius: '6px'
          }}
          href="/"
        >
          Назад
        </Button>
      </Header>
      <Layout hasSider>
        <Content style={contentStyle}>
          <Table
            columns={columns}
            dataSource={data}
            pagination={false}
          />
        </Content>
      </Layout>
      <Footer style={footerStyle}>

      </Footer>
    </Layout>
  );
}

export default ComparisonCity
