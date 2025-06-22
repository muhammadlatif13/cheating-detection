export interface MenuItem {
    name: string;
    link: string;
  }
  
  export const menuList: MenuItem[] = [
    {
      name: 'Detection',
      link: '/menu/detection',
    },
    {
      name: 'Logs',
      link: '/menu/logs',
    },
  ];