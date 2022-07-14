/*
 * @Descripttion: 
 * @version: 
 * @Author: 冉勇
 * @Date: 2022-07-12 17:48:22
 * @LastEditTime: 2022-07-12 17:48:30
 */
const foods = [
    { id: 'husky', title: '哈士奇狗', price: 50, nums: 10 },
    { id: 'car', title: '玩具车', price: 10, nums: 15 },
    { id: 'milk', title: '牛奶', price: 30, nums: 5 },
];
const loadFood = () => {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(foods);
        }, 1000);
    });
};
// @ts-ignore
const getFood = async function () {
    let foods = await loadFood();
    return foods;
};
export default getFood;