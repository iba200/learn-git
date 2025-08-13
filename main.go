package main

import "fmt"

func tri (list [] int ) [] int{
	for i := 0 ; i < len(list); i++ {
		for j := 0; j < len(list); j++ {
			if list[i] < list[j]{
				list[i], list[j] = list[j], list[i]
			}
		}
	}
	return list
}


func main (){
	fmt.Println("Hello, World!")
	numbers := [] int {5 ,1 ,0 ,9 ,6 ,3 ,2 ,8 ,4 ,7}
	fmt.Println("numbers: ", numbers)
	triList := tri(numbers)
	fmt.Println("numbers: ", triList)
}