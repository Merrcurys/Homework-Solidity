// SPDX-License-Identifier: GPL-3.0 
 
pragma solidity >=0.7.0 <0.9.0; 

contract EstateAgency { 
 
    enum EstateType { House, Flat, Loft } 
    enum AdStatus { Opened, Closed } 
 
    // Недвижимость
    struct Estate{ 
        uint size; // Площадь
        string addressEstate; // Адресс 
        address owner; // Владелец
        EstateType esType; // Тип (дом, квартира, лофт)
        bool isActive; // Статус (активно или нет)
        uint idEstate; // id недвижимости
    } 
 
    // Объявление
    struct Advertisement{ 
        address owner; // Продавец
        address buyer; // Покупатель
        uint amount; // Стоимость
        uint idEstate; // id недвижимости
        uint idAd; // id объявления
        uint dateTime; // Дата создания
        AdStatus adStatus; // Статус (открыто или закрыто)
    } 
 
    Estate[] private estates; 
    Advertisement[] private ads; 
 
    mapping (address=>uint) private balance; 
 
    // эвенты
    event paid(address _from, uint _amount); 
    event createdEstate(address owner, uint idEstate  , uint dateTime, EstateType esType); 
    event createdAd(address owner, uint idEstate, uint idAd, uint dateTime, uint amount); 
    event updatedEstate(address owner, uint idEstate, uint dateTime, bool isActive); 
    event updatedAd(address owner, uint idEstate, uint idAd, uint dateTime, AdStatus adStatus); 
    event estatePurchased(address owner, address buyer, uint idEstate, uint idAd, AdStatus adStatus, uint dateTime, uint amount); 
    event fundsBack(address to, uint amount, uint dateTime); 
 
    modifier enoughValue(uint value, uint amount) { 
        require(value >= amount, unicode"У вас недостаточно средств!"); 
        _; 
    } 
 
    modifier onlyEstateOwner(uint idEstate) { 
        require(estates[idEstate].owner == msg.sender, unicode"Вы не владелец данной недвижимости!"); 
        _; 
    } 
 
    modifier onlyAdOwner(uint idAdd) { 
        require(ads[idAdd].owner == msg.sender, unicode"Вы не владелец данного объявления!"); 
        _; 
    } 
 
    modifier isActiveEstate(uint idEstate) { 
        require(estates[idEstate].isActive, unicode"Данная недвижимость недоступна!"); 
        _; 
    } 
 
    modifier isClosedAd(uint idAdd) { 
        require(ads[idAdd].adStatus == AdStatus.Opened, unicode"Данное объявление закрыто!"); 
        _; 
    } 
 
    function createEstate(uint size, string memory addressEstate, EstateType esType) public { 
        require(size > 2, "size must be > 2"); 
        estates.push(Estate(size, addressEstate, msg.sender, esType, true, estates.length)); 
        emit createdEstate(msg.sender, estates.length, block.timestamp, esType); 
    } 
 
    function createAduint(address buyer, uint amount, uint idEstate) public onlyEstateOwner(idEstate) isActiveEstate(idEstate) { 
        require(msg.sender != buyer, unicode"Вы являетесь владельцем недвижимости!");
        ads.push(Advertisement(msg.sender, buyer, amount * 1000000000000000000, idEstate, ads.length, block.timestamp, AdStatus.Opened)); 
        emit createdAd(msg.sender, idEstate, ads.length, block.timestamp, amount * 1000000000000000000); 
    } 
 
    function updateEstateStatus( uint idEstate) public onlyEstateOwner(idEstate) { 
       address owner = msg.sender; 
       emit updatedEstate(owner, idEstate, block.timestamp, estates[idEstate].isActive);
       for (uint i = 0; i < ads.length; i++) { 
            if (ads[i].idEstate == idEstate) { 
                updateAdStatus(idEstate, i); 
                emit updatedAd(msg.sender, idEstate, ads[i].idAd, block.timestamp, AdStatus.Closed); 
            } 
        }
        
        estates[idEstate].isActive = false;  
    } 

    function updateAdStatus( uint idEstate, uint idAd) public onlyEstateOwner (idEstate) isActiveEstate(idEstate) { 
        ads[idAd].adStatus = AdStatus.Closed; 
        emit updatedAd(msg.sender, idEstate, idAd, block.timestamp, AdStatus.Closed); 
    } 

    function buyEstate(uint idAdd) public payable enoughValue(balance[msg.sender] + msg.value, ads[idAdd].amount) { 
        require(msg.sender == ads[idAdd].buyer, unicode"Вы не учавствуете в объявлении как покупатель!");
        balance[msg.sender] += (msg.value - ads[idAdd].amount);
        balance[ads[idAdd].owner] += ads[idAdd].amount;
        estates[ads[idAdd].idEstate].owner = msg.sender;
        updateEstateStatus(ads[idAdd].idEstate); 
        emit paid(msg.sender, ads[idAdd].amount); 
        emit fundsBack(msg.sender, ads[idAdd].amount, block.timestamp); 
    } 
 
    function withDraw(address payable to, uint amount) public payable enoughValue(balance[msg.sender], amount * 1000000000000000000) { 
        balance[msg.sender] -= amount * 1000000000000000000;
        to.transfer(amount * 1000000000000000000); 
    } 

    function getBalance() public view returns(uint) { 
        return balance[msg.sender]; 
    } 
 
    function getEstate() public view returns(Estate[] memory) { 
        return estates; 
    } 
 
    function getAds() public view returns(Advertisement[] memory) { 
        return ads; 
    } 
} 